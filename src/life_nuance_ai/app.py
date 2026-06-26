from __future__ import annotations

from fastapi import FastAPI, HTTPException

from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.router import route_request
from life_nuance_ai.schemas import (
    AssistantDefinition,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)
from life_nuance_ai.seed import seed_assistants


def create_app() -> FastAPI:
    app = FastAPI(
        title="LifeNuance AI",
        version="0.1.0",
        description="Assistant registry and routing platform for nuanced everyday life decisions.",
    )
    registry = AssistantRegistry(seed_assistants())

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", assistant_count=len(registry.list()))

    @app.get("/v1/assistants", response_model=list[AssistantDefinition])
    def list_assistants() -> list[AssistantDefinition]:
        return registry.list()

    @app.post("/v1/assistants", response_model=AssistantDefinition)
    def register_assistant(assistant: AssistantDefinition) -> AssistantDefinition:
        return registry.register(assistant)

    @app.post("/v1/route", response_model=RouteResponse)
    def route(request: RouteRequest) -> RouteResponse:
        try:
            return route_request(request, registry)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    return app
