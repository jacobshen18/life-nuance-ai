from life_nuance_ai.registry import AssistantRegistry
from life_nuance_ai.schemas import AssistantDefinition


def test_registry_registers_and_lists_assistants() -> None:
    registry = AssistantRegistry()
    assistant = AssistantDefinition(
        id="test",
        name="Test Assistant",
        description="A test assistant.",
        domains=["test"],
        keywords=["test"],
        disclaimer="Test only.",
    )

    registry.register(assistant)

    assert registry.get("test") == assistant
    assert registry.list() == [assistant]
