from __future__ import annotations

from life_nuance_ai.schemas import AssistantDefinition


class AssistantRegistry:
    def __init__(self, assistants: list[AssistantDefinition] | None = None) -> None:
        self._assistants: dict[str, AssistantDefinition] = {}
        for assistant in assistants or []:
            self.register(assistant)

    def register(self, assistant: AssistantDefinition) -> AssistantDefinition:
        self._assistants[assistant.id] = assistant
        return assistant

    def list(self) -> list[AssistantDefinition]:
        return sorted(self._assistants.values(), key=lambda assistant: assistant.name)

    def get(self, assistant_id: str) -> AssistantDefinition | None:
        return self._assistants.get(assistant_id)
