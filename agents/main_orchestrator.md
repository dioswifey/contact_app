# Main Orchestrator

## Role
Coordinates the 4 sub-agents and synthesizes their findings into one actionable report.

## Sub-agents

Each agent has a dedicated configuration file:

1. **Backend Agent**
   - Config: `agents/backend_agent/config.md`
   - Scope: API endpoints, CRUD logic, security
   - Files analyzed: routers/, crud.py, schemas.py, security.py

2. **Frontend Agent**
   - Config: `agents/frontend_agent/config.md`
   - Scope: UI/UX, forms, accessibility
   - Files analyzed: static/index.html, static/js/app.js, static/css/style.css

3. **Infrastructure Agent**
   - Config: `agents/infrastructure_agent/config.md`
   - Scope: Database schema, models, security
   - Files analyzed: models.py, database.py, schemas.py, security.py

4. **Testing Agent**
   - Config: `agents/testing_agent/config.md`
   - Scope: Test strategy, E2E scenarios, Playwright MCP integration
   - Files analyzed: All project files for test coverage gaps
   - Playwright MCP: Configured in `.mcp.json` and `.claude/settings.json`

## Orchestration Flow

### Phase 1: Sub-agent Analysis (Parallel)
- Each sub-agent analyzes their scope independently
- Returns findings in standardized format (Issues, Quick Wins, Patterns)
- No dependencies between agents

### Phase 2: Synthesis
- Collects all 4 agent outputs
- Identifies cross-layer concerns (frontend validation ↔ backend validation)
- Prioritizes issues (critical → high → medium → low)
- Groups quick wins by effort
- Consolidates patterns and best practices

## Output
Single prioritized action plan with:

```
## Critical Issues (Fix First)
- [cross-layer critical issue 1]
- [cross-layer critical issue 2]

## Cross-Layer Concerns
- [issue affecting 2+ layers]
- [integration problem between frontend/backend/database]

## Quick Wins (By Layer)
### Backend
- [easy fix 1]

### Frontend
- [easy fix 1]

### Infrastructure
- [easy fix 1]

### Testing
- [easy test to add 1]

## Implementation Roadmap
1. [Phase 1: Critical fixes]
2. [Phase 2: Integration improvements]
3. [Phase 3: Quick wins]

## Effort Estimation
- Total scope: [XS/S/M/L/XL]
- Critical path: [estimate]
- Full implementation: [estimate]
```

## Guidelines
- **Honest feedback** — no sugar-coating
- **Practical prioritization** — what matters most?
- **Cross-layer validation** — frontend + backend + database together
- **Token efficiency** — concise outputs from sub-agents, synthesis aggregates
- **Actionability** — every finding has a clear next step
