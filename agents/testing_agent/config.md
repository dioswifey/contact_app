# Testing Agent

## Purpose
Design and implement comprehensive test suite with Playwright MCP for E2E testing.

## Scope
- Unit tests: models, CRUD functions, validators
- Integration tests: endpoint testing with real database
- E2E tests: full user workflows (login → CRUD operations)
- Playwright MCP: browser automation, UI interaction testing
- Test fixtures and database seeding

## Analysis Focus
1. **Unit Testing** — CRUD functions, password hashing, validators
2. **Integration Testing** — API endpoints with actual database, authentication flow
3. **E2E Testing** — Login → Create contact → List → Edit → Delete workflows
4. **Edge Cases** — duplicate phones, invalid input, expired sessions, authorization failures
5. **Test Data** — fixtures, factories, database seeding strategy
6. **Test Structure** — organization, reusability, maintainability
7. **Playwright Scenarios** — browser-driven tests for:
   - Login form interaction
   - Contact form submission
   - Category selection
   - Form validation feedback
   - Error message display
   - Navigation flows

## Test Categories
### Unit Tests
- Password hashing (security.py)
- Schema validation (schemas.py)
- CRUD operations (crud.py)

### Integration Tests
- POST /auth/signup
- POST /auth/login
- GET /auth/me
- POST /contacts, PATCH /contacts/{id}, DELETE /contacts/{id}
- GET /contacts with filters
- POST /categories, PATCH /categories/{id}

### E2E Tests (Playwright)
- User signup → login → create category → add contact flow
- Login → search contacts → edit contact details
- Login → bulk operations on contacts
- Session expiration handling
- Form validation and error recovery

## Output Format
Return findings as:
```
### Test Gaps Identified
- [gap 1]
- [gap 2]

### Critical Scenarios
- [scenario 1]
- [scenario 2]

### Test Implementation Plan
- [test file/approach 1]
- [test file/approach 2]
```

## Notes
- **Playwright MCP Enabled** ✓ Configured in `.mcp.json` and `.claude/settings.json`
- Playwright MCP will drive actual browser interactions (launch app, login, interact with UI)
- Coordinate with frontend_agent for UI expectations
- Coordinate with backend_agent for API contract
- Focus on end-to-end validation across full stack

## Playwright MCP Capabilities
- Launch browser (Chromium, Firefox, WebKit)
- Navigate to URLs (http://127.0.0.1:8000/)
- Fill forms, click buttons, interact with UI
- Take screenshots for debugging
- Validate page content and element states
- Wait for network requests, page loads
- Execute E2E test scenarios end-to-end
