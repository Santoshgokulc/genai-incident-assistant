# Phase 0: Environment Setup & Progress Log

**Date:** November 15, 2026  
**Curriculum Alignment:** Phase 0 — Environment Setup & Python Muscle Memory (Days 1–3)  
**Status:** Infrastructure Complete & Version Control Setup → Advancing to Drill 1  

---

## 1. Environment & Dependency Management (`uv`)
- **Python Version:** CPython 3.12.16 managed via `.python-version` and `uv`.
- **Core Dependencies:**
  - `fastapi[standard]`: High-performance ASGI framework with standard CLI and server tools (`uvicorn`, `starlette`).
  - `pydantic-settings`: Strict type-validated environment settings loading.
  - `asyncpg`: Native Cython PostgreSQL client using binary wire protocol (no host `libpq` dependency).
  - `redis`: High-speed Redis client supporting async connection pools.
- **Development Tooling:**
  - `ruff`: Code formatting and linting.
  - `pytest`, `pytest-asyncio`, `httpx`: Test runner with async event loop execution and in-memory ASGI client.

---

## 2. Directory Layout & Scaffolding
Aligned repository layout to match clean architecture specifications:
- `src/app/`: Core application modules (`core/`, `schemas/`, `repositories/`, `services/`, `api/v1/`).
- `drills/`: Sequential muscle-memory drills (`drill_1_logs.py`, `drill_2_schemas.py`, `drill_3_health.py`).
- `tests/`: Automated test suite (`test_drills.py`, `test_health.py`, `conftest.py`).
- `learning_history/`: Progress, SOPs, and review tracking.

---

## 3. Local Infrastructure (Docker Compose)
Configured and launched local containerized backend services via `docker-compose.yaml` and `.env`:
- **PostgreSQL 16 (`pgvector/pgvector:pg16`):**
  - Pre-packaged with the `pgvector` C-extension for embedding similarity search.
  - Persistent volume: `postgres_data`
  - Integrated readiness probe: `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}`
- **Redis 7 (`redis:7-alpine`):**
  - In-memory cache and stream broker on Alpine Linux.
  - Persistent volume: `redis_data`
  - Integrated healthcheck: `redis-cli ping`
- **Host Docker Engine Setup:**
  - Configured Docker Engine and Compose plugin on Ubuntu 26.04 LTS.
  - Added user to `docker` group for rootless socket access.
  - Successfully verified container startup via `docker compose up -d`.

---

## 4. Standard Operating Procedure (SOP): GitHub Authentication via PAT

Because GitHub disabled password authentication for Git CLI operations, use this SOP when authenticating HTTPS remotes with a Personal Access Token (PAT).

### Step 1: Generate the Token in GitHub
1. In your browser, navigate to: **GitHub $\rightarrow$ Settings $\rightarrow$ Developer Settings $\rightarrow$ Personal access tokens $\rightarrow$ Tokens (classic)**.
   - Direct link: `https://github.com/settings/tokens`
2. Click **Generate new token** $\rightarrow$ **Generate new token (classic)**.
3. Fill in:
   - **Note:** Descriptive name (e.g. `workstation-linux-cli`).
   - **Expiration:** Choose your preferred duration (e.g., 30, 60, or 90 days).
   - **Scopes:** Select **`repo`** (Full control of private repositories: repo status, repo deployment, public_repo, repo:invite, security_events).
4. Scroll to the bottom and click **Generate token**.
5. **Immediate Action:** Copy the token string (`ghp_...`). It will never be displayed again.

### Step 2: Configure Git Remote & Push
1. Ensure your local branch is `main`:
   ```bash
   git branch -M main
   ```
2. Link the HTTPS remote if not already linked:
   ```bash
   git remote add origin https://github.com/<your-username>/genai-incident-assistant.git
   # Or update existing remote:
   # git remote set-url origin https://github.com/<your-username>/genai-incident-assistant.git
   ```
3. Push to remote:
   ```bash
   git push -u origin main
   ```
4. When prompted by the CLI:
   - **Username:** Your GitHub username.
   - **Password:** Paste the token (`ghp_...`). *(Characters will not echo on screen for security)*.

### Step 3: (Optional) Cache Credentials Locally
To avoid pasting the token on every `git push`/`git pull`:
```bash
# Cache in memory for 1 hour (3600 seconds)
git config --global credential.helper "cache --timeout=3600"

# Or store securely on disk (unencrypted plain text in ~/.git-credentials)
# git config --global credential.helper store
```

---

## 5. Completed Drills & Current Milestone
- **Drill 1: Unstructured Log Ingestion & Cascade Detection** (`drills/drill_1_logs.py`) — **COMPLETED & VERIFIED** ✅
  - Implemented immutable `LogEntry` dataclass, named-group regex parsing (`parse_log_line`), list comprehension filtering (`filter_logs_by_level`), and $O(n)$ frequency aggregation (`calculate_error_rates`).
  - Full retrospective & cheatsheet documented in [drill_1_summary.md](file:///home/user/Projects/genai-incident-assistant/learning_history/drill_1_summary.md).
- **Drill 2: Incident Schema Validation & State Transitions** (`drills/drill_2_schemas.py`) — **COMPLETED & VERIFIED** ✅
  - Implemented deterministic FSM transitions (`validate_incident_transitions`), `IncidentReport` dataclass with `field(default_factory=list)`, `__post_init__` severity validation, `transition_to` lifecycle state updates, `to_dict` serialization via `asdict`, and $O(n)$ key-based deduplication (`deduplicate_incidents`).
  - Full retrospective & cheatsheet documented in [drill_2_summary.md](file:///home/user/Projects/genai-incident-assistant/learning_history/drill_2_summary.md).
- **Active Task:** **Drill 3: Backend Health Checks & Redis/Postgres Status Probes** (`drills/drill_3_health.py`).
  - **Rule Enforcement:** Zero AI code generation; user authoring 100% of the implementation followed by mentor code review.
