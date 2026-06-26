from __future__ import annotations

from life_nuance_ai.schemas import AssistantDefinition


def seed_assistants() -> list[AssistantDefinition]:
    return [
        AssistantDefinition(
            id="education-planner",
            name="Education Planner",
            description="Helps plan learning paths, course choices, tutoring strategy, and skill development.",
            domains=["education", "learning", "career"],
            keywords=[
                "school",
                "course",
                "college",
                "study",
                "tutor",
                "learning",
                "career",
                "certificate",
            ],
            disclaimer="Planning and coaching support only. It does not guarantee admission, grades, or career outcomes.",
            intake_questions=[
                "What is the learner's current level?",
                "What outcome are you aiming for?",
                "What time, budget, and location constraints matter?",
            ],
            handoff_triggers=["special education evaluation", "school legal dispute"],
        ),
        AssistantDefinition(
            id="legal-info-navigator",
            name="Legal Information Navigator",
            description="Helps organize legal questions, documents, timelines, and questions for a qualified lawyer.",
            domains=["legal", "documents", "rights"],
            keywords=[
                "law",
                "legal",
                "contract",
                "lease",
                "tenant",
                "lawsuit",
                "document",
                "court",
            ],
            disclaimer="General legal information only. It is not legal advice and does not create an attorney-client relationship.",
            intake_questions=[
                "What jurisdiction or location is involved?",
                "What documents or deadlines exist?",
                "What outcome are you trying to understand?",
            ],
            handoff_triggers=["court deadline", "criminal matter", "served papers", "eviction notice"],
        ),
        AssistantDefinition(
            id="property-project-planner",
            name="Property Project Planner",
            description="Helps plan home projects, remodel scope, contractor questions, budgets, permits, and risks.",
            domains=["property", "home", "remodel"],
            keywords=[
                "home",
                "house",
                "remodel",
                "contractor",
                "permit",
                "kitchen",
                "bathroom",
                "property",
                "renovation",
            ],
            disclaimer="Planning support only. Verify permits, structural issues, safety, and contracts with qualified professionals.",
            intake_questions=[
                "What space or system are you changing?",
                "What budget and timeline do you have?",
                "Are permits, structural work, electrical, plumbing, or HOA rules involved?",
            ],
            handoff_triggers=["structural change", "electrical hazard", "permit violation", "contract dispute"],
        ),
        AssistantDefinition(
            id="local-activity-guide",
            name="Local Activity Guide",
            description="Helps plan local activities based on location, time, budget, weather, and preferences.",
            domains=["local", "activities", "travel"],
            keywords=[
                "weekend",
                "restaurant",
                "activity",
                "kids",
                "family",
                "date",
                "local",
                "nearby",
                "travel",
            ],
            disclaimer="Recommendations may change. Verify hours, safety, accessibility, prices, and availability.",
            intake_questions=[
                "Who is going?",
                "What area and time window should be considered?",
                "What budget, mobility, weather, or preference constraints matter?",
            ],
            handoff_triggers=["medical emergency", "unsafe location", "severe weather"],
        ),
    ]
