from life_nuance_ai.training import TrainingExample, TrainedRouter, train_router


def test_train_router_predicts_assistant() -> None:
    artifact = train_router(
        [
            TrainingExample(
                message="kitchen remodel permit contractor",
                assistant_id="property-project-planner",
                risk_level="medium",
                handoff_required=False,
            ),
            TrainingExample(
                message="lease tenant contract lawyer",
                assistant_id="legal-info-navigator",
                risk_level="high",
                handoff_required=True,
            ),
        ]
    )
    router = TrainedRouter(artifact)

    prediction = router.predict("I need contractor questions for a remodel permit")

    assert prediction.assistant_id == "property-project-planner"
    assert prediction.risk_level == "medium"
