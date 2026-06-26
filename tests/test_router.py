from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.router import route_request
from life_nuance_ai.schemas import RouteRequest
from life_nuance_ai.seed import seed_assistants
from life_nuance_ai.training import TrainingExample, TrainedRouter, train_router


def test_routes_property_request_to_property_assistant() -> None:
    registry = AssistantRegistry(seed_assistants())
    request = RouteRequest(
        user_id="user-1",
        message="I need help with a kitchen remodel permit and contractor questions.",
        location="Seattle, WA",
    )

    response = route_request(request, registry)

    assert response.assistant.id == "property-project-planner"
    assert "permit" in response.matched_keywords
    assert response.disclaimer


def test_routes_legal_request_to_legal_assistant() -> None:
    registry = AssistantRegistry(seed_assistants())
    request = RouteRequest(
        user_id="user-1",
        message="I need help understanding a lease contract and tenant rights.",
    )

    response = route_request(request, registry)

    assert response.assistant.id == "legal-info-navigator"
    assert response.handoff_triggers


def test_trained_router_is_used_when_available() -> None:
    registry = AssistantRegistry(seed_assistants())
    artifact = train_router(
        [
            TrainingExample(
                message="college learning course plan",
                assistant_id="education-planner",
                risk_level="low",
                handoff_required=False,
            ),
            TrainingExample(
                message="contract lease tenant notice",
                assistant_id="legal-info-navigator",
                risk_level="high",
                handoff_required=True,
            ),
        ]
    )
    trained_router = TrainedRouter(artifact)

    response = route_request(
        RouteRequest(user_id="user-1", message="help me with a lease notice"),
        registry,
        trained_router=trained_router,
    )

    assert response.routing_method == "trained"
    assert response.assistant.id == "legal-info-navigator"
    assert response.handoff_required
