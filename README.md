# AI Travel Planner

A full-stack travel planning platform built around a coordinated **multi-agent AI system**. Given a single natural-language description of a trip, it researches real flights and hotels, checks live weather, finds nearby attractions, estimates a budget, generates a day-by-day itinerary, and produces personalized recommendations — all in one request. A Retrieval-Augmented Generation (RAG) memory layer lets it remember each user's travel preferences across sessions and quietly personalize future plans.

Beyond the AI planning pipeline, the platform includes a full authenticated, multi-user backend with a persistent relational data layer for structured trip management (trips, itineraries, activities, budgets, expenses), and a Python-based interactive frontend.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone & configure](#1-clone--configure)
  - [2. Backend setup](#2-backend-setup)
  - [3. One-time Qdrant setup (RAG memory)](#3-one-time-qdrant-setup-rag-memory)
  - [4. Frontend setup](#4-frontend-setup)
- [Environment Variables](#environment-variables)
- [API Overview](#api-overview)
- [The Multi-Agent Planning System](#the-multi-agent-planning-system)
- [RAG & Long-Term Memory](#rag--long-term-memory)
- [Known Gaps](#known-gaps)
- [Roadmap](#roadmap)

---

## Features

- **One-request trip planning** — describe a trip in plain language (or fill in a structured form) and get back a complete plan: weather, attractions, flights, hotel, itinerary, budget, and personalized recommendations.
- **Multi-agent orchestration** — a dependency-aware orchestrator runs eight specialist agents in the correct order, in parallel where possible, and degrades gracefully if any single agent fails.
- **Personalization via RAG** — a vector-backed long-term memory (Qdrant + Cohere embeddings) remembers each user's preferences and travel history, and feeds relevant context back into every future planning request.
- **Real external data** — live flight search (Duffel), real hotel content and availability (Hotelbeds/HBX), live weather (Open-Meteo), geocoding (Geoapify), and live currency conversion (Frankfurter) — no mocked data.
- **JWT authentication** — registration, login, and refresh tokens; every protected route, including the AI planning endpoint itself, requires a valid authenticated user.
- **Persistent trip management** — a full relational schema and CRUD REST API for trips, itineraries, activities, budgets, and expenses, independent of any single AI planning run.
- **Interactive dashboard** — per-agent execution status and confidence, the generated itinerary, flight/hotel picks with alternatives, a full budget breakdown, and the option to edit, regenerate, export, or manually add an activity to a plan.
- **Observability built in** — every agent's reasoning step is wrapped in an OpenTelemetry span, with OpenLIT auto-instrumenting LLM calls.

---

## Architecture

The platform is organized into two complementary layers sharing the same authenticated backend:

1. **An autonomous multi-agent AI planning pipeline** that turns one natural-language request into a complete, personalized trip plan.
2. **A persistent relational data layer** (Trips, Itineraries, Activities, Budgets, Expenses) with full CRUD REST APIs for structured, ongoing trip management.

### Request flow

```
Frontend (NiceGUI)
   │  structured trip request + JWT
   ▼
FastAPI  →  get_current_user (JWT auth)
   ▼
Planner Service  →  AgentState (input + user_id)
   ▼
Planner Agent
   │  1. retrieve relevant memories for this user (Qdrant)
   │  2. extract structured trip intent via LLM (Groq)
   │  3. write new preference signals back to memory
   ▼
Orchestrator
   │  builds an ExecutionPlan + TaskGraph from the trip intent
   │  Scheduler runs whichever agents are "ready" (deps satisfied)
   ▼
Weather · Attraction · Recommendation · Flight · Hotel · Itinerary · Budget
   │  (each returns a standardized AgentResult: success, result,
   │   confidence, execution_time, error)
   ▼
Aggregated response  →  Dashboard
```

The backend follows clean architecture conventions: a **Repository Pattern** for data access, a **Service Layer** for business logic, and **Dependency Injection** (via FastAPI's `Depends`) for wiring database sessions and the authenticated user into every route.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend framework | FastAPI (Python) | Async REST API |
| ORM / Migrations | SQLAlchemy 2.0 + Alembic | Relational data modeling & schema migrations |
| Database | PostgreSQL | Primary relational store |
| Authentication | JWT (`python-jose`) + bcrypt (`passlib`) | Access/refresh tokens, secure password hashing |
| LLM provider | Groq — Llama 3.3 70B Versatile | Trip-intent extraction, itinerary & recommendation generation |
| Vector database | Qdrant Cloud | Long-term semantic memory (RAG) |
| Embeddings | Cohere `embed-v4.0` (1536-dim) | Turns memories/queries into vectors |
| Flights | Duffel API | Real flight search & pricing |
| Hotels | Hotelbeds / HBX API | Hotel content, live availability & pricing |
| Weather | Open-Meteo API | Geocoding & forecasts |
| Geocoding | Geoapify API | Coordinates for proximity search |
| Currency | Frankfurter API | Live currency conversion |
| Observability | OpenTelemetry + OpenLIT | Distributed tracing, LLM call instrumentation |
| Frontend | NiceGUI (Python) | Reactive, server-rendered UI — no separate JS build |
| HTTP client | httpx | Async calls to all external APIs |

---

## Project Structure

```
traveller/
├── backend/
│   ├── app/
│   │   ├── agents/            # One folder per specialist agent
│   │   │   ├── planner/       #   trip-intent extraction + RAG orchestration
│   │   │   ├── weather/       #   forecasts & travel advice
│   │   │   ├── attraction/    #   nearby points of interest
│   │   │   ├── recommendation/#   personalized picks from attraction candidates
│   │   │   ├── flight/        #   Duffel flight search
│   │   │   ├── hotel/         #   Hotelbeds hotel search
│   │   │   ├── itinerary/     #   day-by-day plan synthesis
│   │   │   ├── budget/        #   cost estimate & currency conversion
│   │   │   ├── memory/        #   embedding service + Qdrant memory store
│   │   │   └── base/          #   shared BaseAgent / AgentState / AgentResult
│   │   ├── orchestrator/      # ExecutionPlan, TaskGraph, Scheduler, Executor
│   │   ├── api/v1/routes/     # FastAPI routers (auth, trips, planner, ...)
│   │   ├── services/          # Business logic (AuthService, PlannerService, ...)
│   │   ├── data/               # Repositories, DB models, cached hotel catalogue
│   │   ├── core/               # Config, security, dependencies, exceptions
│   │   └── observability/      # OpenTelemetry tracer, OpenLIT init
│   ├── alembic/                 # DB migrations
│   ├── create_index.py          # one-time: create Qdrant payload index
│   ├── reset_qdrant.py          # one-time: (re)create the Qdrant collection
│   ├── sync_hotelbeds_hotels.py # populate the local hotel catalogue cache
│   └── requirements.txt
└── frontend/
    ├── pages/                  # landing (trip form), login, dashboard
    ├── components/dashboard/   # agent grid, itinerary, budget/insights, header
    ├── services/                # planner_service, auth_service, dashboard_adapter
    ├── state/                   # sample/dashboard state
    └── main.py                  # NiceGUI entrypoint & route guards
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (running locally or accessible via `DATABASE_URL`)
- A [Qdrant Cloud](https://cloud.qdrant.io/) cluster (free tier works)
- API keys for: Groq, Duffel, Geoapify, Cohere, and Hotelbeds (see [Environment Variables](#environment-variables))

### 1. Clone & configure

```bash
git clone <repo-url>
cd traveller
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# fill in .env with your real keys — see Environment Variables

alembic upgrade head              # apply DB migrations

uvicorn app.main:app --reload --port 8000
```

The API is now running at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### 3. One-time Qdrant setup (RAG memory)

Run these once, after your Qdrant credentials are in `.env`:

```bash
python reset_qdrant.py    # creates the `user_memory` collection
python create_index.py    # indexes `user_id` for per-user filtered search
```

Optional — populate the local hotel catalogue cache used alongside live Hotelbeds lookups:

```bash
python sync_hotelbeds_hotels.py
```

### 4. Frontend setup

In a separate terminal:

```bash
cd frontend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

The app is now running at `http://127.0.0.1:8080`. Register an account, sign in, and plan your first trip.

---

## Environment Variables

Set these in `backend/.env` (see `backend/.env.example` for a template):

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `SECRET_KEY` | ✅ | Long random secret used to sign JWTs |
| `ALGORITHM` | | JWT signing algorithm (default `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | | Access token lifetime (default `30`) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | | Refresh token lifetime (default `7`) |
| `AI_PROVIDER` | | LLM provider (default `groq`) |
| `GROQ_API_KEY` | ✅ | Groq API key for LLM calls |
| `GROQ_MODEL` | | Model name (default `llama-3.3-70b-versatile`) |
| `DUFFEL_API_TOKEN` | ✅ | Duffel API token for flight search |
| `GEOAPIFY_API_KEY` | ✅ | Geoapify API key for geocoding |
| `HOTELBEDS_API_KEY` / `HOTELBEDS_API_SECRET` | ✅ | Hotelbeds/HBX credentials for hotel search |
| `COHERE_API_KEY` | ✅ | Cohere API key for RAG embeddings |
| `QDRANT_URL` / `QDRANT_API_KEY` | ✅ | Qdrant Cloud cluster URL & key for long-term memory |

> No API keys required: Open-Meteo (weather) and Frankfurter (currency) are free, keyless APIs.

The frontend has no required environment variables in development — it talks to the backend at `http://localhost:8000` by default (see `frontend/services/*.py`).

---

## API Overview

| Group | Endpoints | Purpose |
|---|---|---|
| Health | `GET /health` | Liveness check |
| Auth | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` | Account creation, login, current user |
| Planner | `POST /planner/` | Runs the full multi-agent AI planning workflow *(authenticated)* |
| Trips | `GET/POST /trips`, `GET/PUT/DELETE /trips/{id}` | CRUD for persisted trips |
| Itinerary | `GET/POST /itineraries`, `/itinerary-days` | CRUD for structured itineraries |
| Activities | CRUD `/activities` | Individual itinerary activities |
| Budget | CRUD `/budgets` | Per-trip budget breakdown |
| Expenses | CRUD `/expenses` | Logged spending against a trip |
| Dashboard | `GET /dashboard/{trip_id}` | Aggregated budget/expense/itinerary summary |

Full interactive documentation is available at `/docs` (Swagger) once the backend is running.

---

## The Multi-Agent Planning System

Every agent is a small, self-contained module (its own schema, tools, and prompt where relevant) that focuses on exactly one concern, and every agent returns a standardized `AgentResult` — `success`, `result`, `confidence`, `execution_time`, `error` — so the orchestrator can reason uniformly about partial success and failure.

| Agent | Responsibility | Runs when |
|---|---|---|
| **Planner** | Extracts a structured trip intent from free text; retrieves and writes RAG memory | Always — entry point |
| **Weather** | Live weather/forecast for the destination + travel advice | Destination known |
| **Attraction** | Nearby points of interest | Destination known |
| **Recommendation** | Personalizes a shortlist from the Attraction agent's candidates | After Attraction (+ Weather) |
| **Flight** | Real flight search & pricing via Duffel | Origin, destination & start date known |
| **Hotel** | Hotel search via Hotelbeds, live availability & pricing | Destination & full date range known |
| **Itinerary** | Day-by-day plan synthesis via LLM | After Weather, Flight & Hotel |
| **Budget** | Full cost estimate & comparison to stated budget | After Flight, Hotel (and Itinerary if present) |

The **Orchestrator** doesn't run agents in a fixed sequence. It builds an `ExecutionPlan` dynamically from which trip-intent fields are present, converts it into a `TaskGraph` of dependencies, and a `Scheduler` repeatedly runs whichever tasks are currently "ready" until the graph completes — letting independent agents (e.g. Weather, Attraction) run without waiting on each other, while dependent agents (e.g. Itinerary) correctly wait for their inputs.

Four additional agent folders (`restaurant`, `events`, `transportation`, `report`) exist as scaffolding for planned future capabilities but are not yet implemented or registered.

---

## RAG & Long-Term Memory

The Planner Agent remembers each user across sessions:

1. On every planning request, it embeds the current request (Cohere `embed-v4.0`) and queries Qdrant for that user's five most semantically relevant past memories.
2. Those memories are woven into the LLM prompt as long-term user preferences and travel history, with instructions to personalize hotels, attractions, food, and pacing accordingly — while always deferring to the current explicit request if the two conflict.
3. After the trip intent is generated, new preference signals (stated interests, the destination just planned) are extracted and written back to Qdrant as new memories.
4. Memory read/write failures are caught and logged but never block trip planning — personalization is an enhancement, not a hard dependency.

---

## Known Gaps

- `app/rag/` (a separate, broader retrieval module) and `app/evaluation/` (confidence/hallucination scoring harness) exist as empty scaffolding, not yet implemented.
- The `restaurant`, `events`, `transportation`, and `report` agents are scaffolded but not implemented or registered.
- `app/gateway/` (a dedicated API gateway with centralized auth middleware & rate limiting) is scaffolded but not wired in — auth is currently enforced per-route via a shared FastAPI dependency instead.

---

## Roadmap

- Restaurant, Events, and Transportation specialist agents
- A broader destination knowledge base for retrieval-grounded recommendations, beyond per-user memory
- An automated evaluation harness for agent confidence and hallucination scoring
- A dedicated API gateway layer with centralized rate limiting