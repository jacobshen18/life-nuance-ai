from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class TrainingExample:
    message: str
    assistant_id: str
    risk_level: str
    handoff_required: bool


@dataclass(frozen=True)
class RouterPrediction:
    assistant_id: str
    confidence: float
    risk_level: str
    handoff_required: bool
    matched_tokens: list[str]


class TrainedRouter:
    def __init__(self, artifact: dict[str, Any]) -> None:
        self.assistant_priors = artifact["assistant_priors"]
        self.token_counts = artifact["token_counts"]
        self.class_totals = artifact["class_totals"]
        self.vocabulary = set(artifact["vocabulary"])
        self.risk_by_assistant = artifact["risk_by_assistant"]
        self.handoff_by_assistant = artifact["handoff_by_assistant"]

    def predict(self, message: str) -> RouterPrediction:
        tokens = tokenize(message)
        scores: dict[str, float] = {}
        vocab_size = max(1, len(self.vocabulary))

        for assistant_id, prior in self.assistant_priors.items():
            score = math.log(prior)
            total = self.class_totals[assistant_id]
            counts = self.token_counts[assistant_id]
            for token in tokens:
                score += math.log((counts.get(token, 0) + 1) / (total + vocab_size))
            scores[assistant_id] = score

        assistant_id = max(scores.items(), key=lambda item: item[1])[0]
        matched_tokens = sorted(set(tokens) & set(self.token_counts[assistant_id].keys()))
        return RouterPrediction(
            assistant_id=assistant_id,
            confidence=round(_softmax_confidence(scores, assistant_id), 2),
            risk_level=self.risk_by_assistant.get(assistant_id, "low"),
            handoff_required=bool(self.handoff_by_assistant.get(assistant_id, False)),
            matched_tokens=matched_tokens,
        )


def train_router(examples: list[TrainingExample]) -> dict[str, Any]:
    if not examples:
        raise ValueError("Training examples are required.")

    assistant_counts: Counter[str] = Counter()
    token_counts: dict[str, Counter[str]] = defaultdict(Counter)
    class_totals: Counter[str] = Counter()
    risk_votes: dict[str, Counter[str]] = defaultdict(Counter)
    handoff_votes: dict[str, Counter[bool]] = defaultdict(Counter)
    vocabulary: set[str] = set()

    for example in examples:
        tokens = tokenize(example.message)
        assistant_counts[example.assistant_id] += 1
        token_counts[example.assistant_id].update(tokens)
        class_totals[example.assistant_id] += len(tokens)
        risk_votes[example.assistant_id][example.risk_level] += 1
        handoff_votes[example.assistant_id][example.handoff_required] += 1
        vocabulary.update(tokens)

    total_examples = sum(assistant_counts.values())
    return {
        "version": 1,
        "assistant_priors": {
            assistant_id: count / total_examples for assistant_id, count in assistant_counts.items()
        },
        "token_counts": {
            assistant_id: dict(counts) for assistant_id, counts in token_counts.items()
        },
        "class_totals": dict(class_totals),
        "vocabulary": sorted(vocabulary),
        "risk_by_assistant": {
            assistant_id: votes.most_common(1)[0][0] for assistant_id, votes in risk_votes.items()
        },
        "handoff_by_assistant": {
            assistant_id: votes.most_common(1)[0][0] for assistant_id, votes in handoff_votes.items()
        },
        "training_examples": total_examples,
    }


def load_examples(path: Path) -> list[TrainingExample]:
    examples: list[TrainingExample] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            record = json.loads(stripped)
            try:
                examples.append(
                    TrainingExample(
                        message=str(record["message"]),
                        assistant_id=str(record["assistant_id"]),
                        risk_level=str(record["risk_level"]),
                        handoff_required=bool(record["handoff_required"]),
                    )
                )
            except KeyError as error:
                raise ValueError(f"{path}:{line_number} missing field: {error}") from error
    return examples


def save_artifact(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_router(path: Path) -> TrainedRouter:
    return TrainedRouter(json.loads(path.read_text(encoding="utf-8")))


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def _softmax_confidence(scores: dict[str, float], selected: str) -> float:
    max_score = max(scores.values())
    exp_scores = {key: math.exp(value - max_score) for key, value in scores.items()}
    denominator = sum(exp_scores.values())
    return 0.0 if denominator == 0 else exp_scores[selected] / denominator
