from __future__ import annotations

from pydantic import BaseModel, Field


class AssistantDefinition(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    domains: list[str] = Field(min_length=1)
    keywords: list[str] = Field(default_factory=list)
    disclaimer: str = Field(min_length=1)
    intake_questions: list[str] = Field(default_factory=list)
    handoff_triggers: list[str] = Field(default_factory=list)


class RouteRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    location: str | None = None
    constraints: dict[str, str] = Field(default_factory=dict)


class RouteResponse(BaseModel):
    assistant: AssistantDefinition
    confidence: float = Field(ge=0.0, le=1.0)
    matched_keywords: list[str]
    disclaimer: str
    suggested_next_steps: list[str]
    intake_questions: list[str]
    handoff_triggers: list[str]


class HealthResponse(BaseModel):
    status: str
    assistant_count: int
