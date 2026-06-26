from fastapi.testclient import TestClient

from life_nuance_ai.app import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["assistant_count"] >= 4


def test_route_endpoint() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/route",
        json={
            "user_id": "demo",
            "message": "Help me plan a college learning path for machine learning.",
        },
    )

    assert response.status_code == 200
    assert response.json()["assistant"]["id"] == "education-planner"


def test_register_assistant_endpoint() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/assistants",
        json={
            "id": "finance-planner",
            "name": "Finance Planner",
            "description": "Helps organize financial planning questions.",
            "domains": ["finance"],
            "keywords": ["budget", "saving"],
            "disclaimer": "Planning support only, not financial advice.",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == "finance-planner"
