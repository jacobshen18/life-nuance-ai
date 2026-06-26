from __future__ import annotations

import re

from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.schemas import AssistantDefinition, RouteRequest, RouteResponse


def route_request(request: RouteRequest, registry: AssistantRegistry) -> RouteResponse:
    candidates = registry.list()
    if not candidates:
        raise ValueError("No assistants are registered.")

    scored = [_score_assistant(request.message, assistant) for assistant in candidates]
    scored.sort(key=lambda item: item[0], reverse=True)
    score, assistant, matched_keywords = scored[0]
    confidence = min(1.0, round(score / 5, 2))

    return RouteResponse(
        assistant=assistant,
        confidence=confidence,
        matched_keywords=matched_keywords,
        disclaimer=assistant.disclaimer,
        suggested_next_steps=_next_steps(assistant, request),
        intake_questions=assistant.intake_questions,
        handoff_triggers=assistant.handoff_triggers,
    )


def _score_assistant(
    message: str,
    assistant: AssistantDefinition,
) -> tuple[int, AssistantDefinition, list[str]]:
    tokens = set(re.findall(r"[a-z0-9]+", message.lower()))
    keywords = {keyword.lower() for keyword in assistant.keywords}
    domains = {domain.lower() for domain in assistant.domains}

    matched_keywords = sorted(tokens & keywords)
    matched_domains = sorted(tokens & domains)
    score = len(matched_keywords) + 2 * len(matched_domains)
    return score, assistant, matched_keywords + matched_domains


def _next_steps(assistant: AssistantDefinition, request: RouteRequest) -> list[str]:
    steps = [
        f"Use the {assistant.name} module for this request.",
        "Answer the intake questions before generating a plan.",
        "Separate facts, assumptions, options, and risks.",
    ]

    if request.location:
        steps.append(f"Account for location-specific constraints in {request.location}.")
    if request.constraints:
        steps.append("Respect the user's stated constraints before suggesting next actions.")
    if assistant.handoff_triggers:
        steps.append("Check whether any handoff trigger requires a qualified professional.")

    return steps
