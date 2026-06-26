from __future__ import annotations

import argparse
from pathlib import Path

from life_nuance_ai.training import load_examples, save_artifact, train_router


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train the LifeNuance assistant router.")
    parser.add_argument("--train-data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/router_model.json"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    examples = load_examples(args.train_data)
    artifact = train_router(examples)
    save_artifact(args.output, artifact)
    print(f"Wrote {args.output} from {artifact['training_examples']} examples")


if __name__ == "__main__":
    main()
