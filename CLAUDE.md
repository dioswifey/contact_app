# Contact App — Multi-Agent Code Review & Testing Setup

## Project Overview

This is a **FastAPI + React contact management application** with multi-agent orchestration for code review, testing, and quality assurance.

- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **Database**: PostgreSQL
- **Architecture**: User-isolated contact + category management system

## Multi-Agent Structure

This project uses a **4-agent orchestration system** to analyze code quality, identify issues, and plan improvements across different layers.

### 📌 Start Here: `agents/main_orchestrator.md`

Read this file first to understand how the agents work together and what to expect from a multi-agent analysis run.

**Key Contents:**
- Sub-agent descriptions and file locations
- Orchestration flow (parallel analysis → synthesis)
- Output format and guidelines
- How findings are prioritized

### 🤖 Agent Locations

Each agent has its own configuration directory:

```
agents/
├── backend_agent/config.md          # API, CRUD, security analysis
├── frontend_agent/config.md         # UI/UX, forms, accessibility
├── infrastructure_agent/config.md   # Database, models, schema
├── testing_agent/config.md          # Test gaps, E2E scenarios (Playwright MCP)
└── main_orchestrator.md             # ← Start here
```

### 🎬 Running Multi-Agent Analysis

To run the full multi-agent orchestrator workflow:

1. Ensure Playwright MCP is configured (see `./mcp.json` and `./.claude/settings.json`)
2. Invoke the orchestrator workflow (instructions in main_orchestrator.md)
3. Review the synthesized action plan with prioritized findings

### 📋 Current Status

- ✅ Multi-agent framework set up
- ✅ Playwright MCP configured for E2E testing
- ✅ 4 specialized agents ready (backend, frontend, infrastructure, testing)
- ⏳ Ready to run first orchestrator analysis

### 🔗 Related Files

- `.mcp.json` — Playwright MCP server configuration
- `.claude/settings.json` — Project MCP settings
- Original code structure: `models.py`, `crud.py`, `routers/`, `static/`

---

**For detailed agent instructions, see: `agents/main_orchestrator.md`**
