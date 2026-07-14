# Infrastructure Agent

## Purpose
Review database schema, models, security, and data integrity concerns.

## Scope
- `models.py` — table definitions (User, LoginSession, Category, Contact)
- `database.py` — connection setup, engine configuration
- `schemas.py` — Pydantic validation schemas
- `security.py` — password hashing (Argon2)
- Constraints, relationships, indexes
- Data types and nullable fields
- Migration strategy and scaling

## Analysis Focus
1. **Schema Design** — table structure, data types, constraints
2. **Relationships** — foreign keys, cascading behavior, referential integrity
3. **Constraints** — unique constraints (user+phone, user+category_name), primary keys
4. **Query Efficiency** — N+1 queries, missing indexes, query optimization
5. **Security** — password hashing, user_id isolation, SQL injection prevention
6. **Data Integrity** — nullable fields, default values, validation at DB layer
7. **Scaling** — migration strategy, performance bottlenecks

## Output Format
Return findings as:
```
### Issues Found
- [issue 1]
- [issue 2]

### Optimizations
- [optimization 1]
- [optimization 2]

### Patterns (Good Practices)
- [good pattern 1]
```

## Notes
- PostgreSQL 16 is the target database
- Focus on data integrity and query performance
- Coordinate with backend_agent for CRUD usage patterns
- Document any schema changes needed for testing_agent scenarios
