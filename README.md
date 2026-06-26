# LifeNuance AI

LifeNuance AI is a platform for registering and routing specialized AI assistants for everyday life decisions.

The project starts with a simple assistant registry and routing API. Users describe what they need, and the platform recommends an assistant module with domain boundaries, required disclaimers, and a structured next-step plan.

## Initial Assistant Domains

- Education planning: learning goals, course planning, tutoring strategy, career learning paths
- Legal information navigator: issue triage, document checklist, questions to ask a qualified lawyer
- Property and home projects: remodel planning, contractor questions, budget/risk checklists
- Local activities: family activities, city exploration, weekend planning, constraints-aware recommendations

## Important Boundaries

LifeNuance AI provides planning support and general information. It does not replace licensed professionals.

- Legal module: informational guidance only, not legal advice.
- Property module: planning support only, not engineering, permitting, or contractor certification.
- Education module: planning and coaching support only, not school admissions guarantees.
- Local activity module: recommendations should verify hours, safety, prices, and availability.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn life_nuance_ai.app:create_app --factory --reload
```

Try routing a request:

```bash
curl -X POST http://localhost:8000/v1/route \
  -H "Content-Type: application/json" \
  -d @examples/route_request.json
```

Register a new assistant:

```bash
curl -X POST http://localhost:8000/v1/assistants \
  -H "Content-Type: application/json" \
  -d @examples/register_assistant.json
```

## API

- `GET /health`
- `GET /v1/assistants`
- `POST /v1/assistants`
- `POST /v1/route`

## Product Direction

The first product wedge is not a generic chatbot. It is a trusted registry of life-domain assistants with:

- explicit domain scopes
- professional-boundary rules
- structured intake questions
- routing based on user intent
- safety disclaimers and escalation guidance

Over time, each assistant can be backed by curated tools, local data, document workflows, and domain-specific evaluation.

## License

MIT
