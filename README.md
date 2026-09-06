# FocusGroup.AI 🤖💬

An open-source multi-agent simulation engine built to run intense, realistic focus group debates for evaluating naming and product decisions. The architecture implements a structured **Planner-Executor-Critic** topology utilizing **LangGraph** for orchestration, **LangChain** for LLM execution components, and **LangSmith** for full production-grade observability.

This platform allows users to input a core company context and test up to **5 options** against up to **5 stateful AI personas (ICPs)** that fiercely protect their distinct business interests — then produces a weighted numeric scorecard.

The shipped example config evaluates brand names for [Spectrum Hire](https://spectrumhire.ai), a multi-tool AI hiring suite — but nothing about the engine is specific to that scenario. Every company context, option, and persona is just data you supply.

---

## 🏗️ Tech Stack

- **Backend:** Python 3.10+, FastAPI (asynchronous streaming via WebSockets)
- **Agent Orchestration:** LangGraph, LangChain
- **Observability & Tracing:** LangSmith
- **Frontend:** Node.js, React (functional components, custom hooks for handling live token streams)

---

## 🛠️ System Architecture & Workflow

The simulation runs through a deterministic state machine managed by LangGraph:

1. **Planner Layer:** Receives a `SimulationConfig` and slices the session into 3 sequential evaluation phases:
   - *Phase 1: First Impressions & Domain Recognition*
   - *Phase 2: Friction, Safety, and Trust*
   - *Phase 3: The Verdict (Cross-examination debate)*
2. **Executor Layer:** Runs an iterative loop where each persona reacts to and challenges prior speakers, streaming tokens live over a WebSocket.
3. **Critic Layer:** Scores every option on 4 vectors plus each persona's overall rating, then computes a weighted composite score in code (never left to the LLM to do the arithmetic) — outputting a structured, markdown-rendered scorecard.

```
[ SimulationConfig ] ──> [ Planner Node ] ──> [ Executor Node (loops phases 1-3) ] ──> [ Critic Node ] ──> [ Scorecard ]
```

---

## 🚀 Quick Start & Installation

### 1. Backend Setup (Python & FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Create a `.env` file in `backend/` (see `.env.example`):

```env
OPENAI_API_KEY=your-openai-api-key-here

# LangSmith Observability Setup
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=focusgroup-ai-simulation
LANGCHAIN_API_KEY=your-langsmith-api-key-here

MODEL_NAME=gpt-4o
PORT=8000
```

Start the local FastAPI development server:

```bash
uvicorn main:app --reload --port 8000
```

Run the test suite (no API key required — it runs entirely against a fake LLM):

```bash
pytest
```

### 2. Frontend Setup (Node.js & React)

```bash
cd frontend
npm install
npm start
```

Configure `frontend/.env` from `.env.example` if your backend isn't on `localhost:8000`.

---

## ⚙️ Configuration Model

A `SimulationConfig` is just:

- `company_context` — free text describing the company/product.
- `framework_description` — free text describing what's being evaluated.
- `candidates` — 2 to **5** options under evaluation.
- `personas` — 1 to **5** ICPs (Ideal Customer Profiles), each with a `name`, `description`, and a `weight`. Weights don't need to sum to 1 or 100 — they're auto-normalized (e.g. `45/35/20` → `0.45/0.35/0.20`), and a `config-normalized` event reports the conversion.

The "Load hiring-tool example" button in the UI (or `GET /api/examples/hiring-tool`) loads the shipped Spectrum Hire scenario so you can see a full run without writing a config by hand.

---

## 📊 Scorecard Structure

| Option | Scope Coverage (1-10) | Corporate Safety (1-10) | Modern Edge (1-10) | Storytelling Value (1-10) | Final Composite Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Option A** | *Score* | *Score* | *Score* | *Score* | **Weighted Total** |
| **Option B** | *Score* | *Score* | *Score* | *Score* | **Weighted Total** |

Composite score = `Σ (persona rating × normalized persona weight)`.

---

## 📈 Learning with LangSmith

Point your LangSmith dashboard at the `LANGCHAIN_PROJECT` from `.env` during simulation runs to trace:

- **Graph transitions** — how state passes between Planner, Executor, and Critic.
- **Token streaming** — live per-persona token output during the Executor phases.
- **Prompt behavior** — which persona/phase prompts drive the most interesting arguments.

---

## ⚠️ Known v1 Limitations

This is a first open-source drop, intentionally minimal:

- **No auth.** Anyone who can reach the API can start a simulation.
- **No persistence.** Session state lives in an in-memory dict — restarting the backend loses all in-flight and past sessions.
- **No Docker/CI yet.** Contributions welcome — see below.
- A WebSocket client that connects after a session starts replays the full event log first, then streams live; a client that disconnects and reconnects gets the same replay-then-live behavior, but there's no reconnect/backoff logic built into the frontend yet.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for updates to the graph/state routing, additional evaluation vectors, persistence, auth, CI, or frontend/dashboard enhancements.

## License

MIT — see [LICENSE](./LICENSE).
