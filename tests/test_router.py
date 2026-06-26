from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.router import route_request
from life_nuance_ai.schemas import RouteRequest
from life_nuance_ai.seed import seed_assistants


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
