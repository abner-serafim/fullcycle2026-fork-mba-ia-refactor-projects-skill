# Walkthrough - task-manager-api Refactoring

We have successfully refactored `task-manager-api` to follow the MVC architecture patterns, addressed high-severity security issues, and optimized performance by solving database N+1 query problems.

## Changes Made

### 1. Separation of Concerns (MVC Pattern)
- Created **Controllers** under a new directory `controllers/` to handle all business logic, queries, and request validations:
  - [user_controller.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/controllers/user_controller.py)
  - [task_controller.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/controllers/task_controller.py)
  - [report_controller.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/controllers/report_controller.py)
- Refactored **Routes** to delegate all actions directly to the controllers, removing SQL, validations, and logic from endpoints:
  - [user_routes.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/routes/user_routes.py)
  - [task_routes.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py)
  - [report_routes.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/routes/report_routes.py)

### 2. Configuration & Secrets Isolation
- Created [config.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/config.py) and [.env](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/.env).
- Migrated all hardcoded values (`SECRET_KEY` in `app.py`, SMTP parameters in `notification_service.py`) to env-loaded variables.
- Refactored [app.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/app.py) to load database URI and keys dynamically.

### 3. Password Hashing Security Upgrade
- Replaced the vulnerable `hashlib.md5` with modern `bcrypt` hashing in [user.py](file:///home/abneradekz/projetos/estudo/fullcycle-2026/mba-ia-refactor-projects-skill/task-manager-api/models/user.py).
- Maintained a secure fallback check for old passwords so current seed databases and users do not break.

### 4. Database Performance (N+1 Queries Solved)
- Used eager loading (`db.joinedload`) when retrieving multiple entities to prevent loops from firing separate queries:
  - In `get_tasks` (loading task users and categories in a single query).
  - In `get_users` (loading user tasks count efficiently).
  - In `get_categories` (loading category tasks efficiently).

## Validation Results

We executed the database seeder and booted the dev server inside the local `.venv` environment to verify functionality:
```bash
./.venv/bin/python seed.py
./.venv/bin/python app.py
```

### Health Check `/health`
```json
{
  "status": "ok",
  "timestamp": "2026-06-09 19:56:55.620555"
}
```

### Tasks Retrieval `/tasks`
Successfully fetched tasks with preloaded user name and category name in a single join query, resolving N+1 query loops.
