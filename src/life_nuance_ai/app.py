from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from life_nuance_ai.model_store import load_optional_router
from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.router import route_request
from life_nuance_ai.schemas import (
    AssistantDefinition,
    HealthResponse,
    RouteRequest,
    RouteResponse,
)
from life_nuance_ai.seed import seed_assistants


STATIC_DIR = Path(__file__).parent / "static"


def create_app() -> FastAPI:
    app = FastAPI(
        title="LifeNuance AI",
        version="0.1.0",
        description="Assistant registry and routing platform for nuanced everyday life decisions.",
    )
    registry = AssistantRegistry(seed_assistants())
    trained_router = load_optional_router()

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def demo() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/v1/demo/cases")
    def demo_cases() -> list[dict[str, object]]:
        return _demo_cases()

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
            return route_request(request, registry, trained_router=trained_router)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    return app


def _demo_cases() -> list[dict[str, object]]:
    return [
        {
            "id": "eviction-notice",
            "assistant_id": "legal-info-navigator",
            "label": "Eviction notice",
            "message": "I received an eviction notice in San Diego and need to understand what to do next.",
            "location": "San Diego, CA",
            "constraints": {"role": "tenant", "priority": "deadline-sensitive"},
            "summary": "Organize the notice, identify the current stage, and prepare questions for qualified legal help.",
            "facts": [
                "California calls a residential eviction court case an unlawful detainer.",
                "A written notice comes before a landlord can start an eviction court case.",
                "If court papers have been served, a tenant response may be time-sensitive.",
            ],
            "actions": [
                "Record when and how the notice or court papers were received.",
                "Keep the notice, lease, payment records, and landlord messages together.",
                "Use the California Courts tenant guide to identify the current stage.",
                "Contact a court self-help center or qualified lawyer about deadlines.",
            ],
            "sources": [
                {
                    "title": "Eviction cases in California",
                    "publisher": "California Courts Self-Help Guide",
                    "url": "https://selfhelp.courts.ca.gov/eviction",
                    "checked": "2026-06-30",
                },
                {
                    "title": "The eviction process for tenants",
                    "publisher": "California Courts Self-Help Guide",
                    "url": "https://selfhelp.courts.ca.gov/eviction-tenant",
                    "checked": "2026-06-30",
                },
            ],
        },
        {
            "id": "college-options",
            "assistant_id": "education-planner",
            "label": "Compare colleges",
            "message": "Help me compare affordable computer science programs and plan what data to review.",
            "location": "California",
            "constraints": {"budget": "cost-conscious", "subject": "computer science"},
            "summary": "Build a comparison around cost, completion, field of study, and likely outcomes.",
            "facts": [
                "College Scorecard publishes institution-level cost, completion, and earnings data.",
                "Not every metric is available for every institution or reporting year.",
                "Published outcomes should be interpreted alongside personal fit and program details.",
            ],
            "actions": [
                "Shortlist schools by location, program availability, and net price.",
                "Compare completion and outcome metrics using the same reporting definitions.",
                "Confirm curriculum, transfer rules, and current costs with each institution.",
            ],
            "sources": [
                {
                    "title": "College Scorecard",
                    "publisher": "U.S. Department of Education",
                    "url": "https://collegescorecard.ed.gov/",
                    "checked": "2026-06-30",
                },
                {
                    "title": "College Scorecard data documentation",
                    "publisher": "U.S. Department of Education",
                    "url": "https://collegescorecard.ed.gov/data/documentation/",
                    "checked": "2026-06-30",
                },
            ],
        },
        {
            "id": "kitchen-remodel",
            "assistant_id": "property-project-planner",
            "label": "Kitchen remodel",
            "message": "Plan a San Diego kitchen remodel with permit, budget, and contractor questions.",
            "location": "San Diego, CA",
            "constraints": {"budget": "$45,000", "timeline": "4 months"},
            "summary": "Turn an early remodel idea into a scoped project with permit and contractor checkpoints.",
            "facts": [
                "San Diego Development Services publishes permit guidance and online permitting tools.",
                "Permit needs depend on the work scope, including structural, plumbing, and electrical changes.",
                "A realistic budget should separate construction, design, permits, and contingency.",
            ],
            "actions": [
                "Write a room-by-room scope and identify structural or utility changes.",
                "Check the city permit portal before finalizing contractor bids.",
                "Ask bidders to separate labor, materials, allowances, and exclusions.",
                "Reserve a contingency and define a written change-order process.",
            ],
            "sources": [
                {
                    "title": "Permits and Approvals",
                    "publisher": "City of San Diego Development Services",
                    "url": "https://www.sandiego.gov/development-services/permits",
                    "checked": "2026-06-30",
                }
            ],
        },
        {
            "id": "family-weekend",
            "assistant_id": "local-activity-guide",
            "label": "Family weekend",
            "message": "Find a low-cost outdoor family activity in San Diego for this weekend.",
            "location": "San Diego, CA",
            "constraints": {"budget": "under $40", "group": "two adults and one child"},
            "summary": "Create a weather-aware shortlist using official park and recreation information.",
            "facts": [
                "San Diego Parks and Recreation maintains parks, recreation centers, trails, and programs.",
                "Hours, reservations, fees, and closures can change by facility and date.",
                "The final choice should be verified against current conditions before leaving.",
            ],
            "actions": [
                "Choose a neighborhood radius and preferred activity level.",
                "Check official facility details, hours, parking, and accessibility.",
                "Verify weather and any same-day closure or reservation requirement.",
            ],
            "sources": [
                {
                    "title": "Parks and Recreation",
                    "publisher": "City of San Diego",
                    "url": "https://www.sandiego.gov/park-and-recreation",
                    "checked": "2026-06-30",
                }
            ],
        },
    ]
