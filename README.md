# AgentX 🧠

> Multi-agent research system. Watch them think.

AgentX orchestrates four specialised AI agents that collaborate, challenge each other, and converge on verified answers in real time. Built on the **supervisor pattern** — one orchestrator delegating to specialist subagents — inspired by Anthropic's internal research architecture.

![AgentX Demo](https://img.shields.io/badge/status-active-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Stack](https://img.shields.io/badge/stack-React%20%2B%20FastAPI%20%2B%20Groq-orange)

---

## How It Works

```
User Query
    ↓
Supervisor Agent (orchestrates)
    ↓
┌─────────────┬──────────────┬─────────────┐
Searcher      Synthesiser    Critic
(finds raw    (builds the    (challenges
 evidence)     answer)        the answer)
└─────────────┴──────────────┴─────────────┘
    ↓
Supervisor delivers Final Verdict + Confidence Score
```

Each agent's output feeds the next. The **Critic** specifically attacks the **Synthesiser's** conclusions before the **Supervisor** makes a final call. You watch every step live.

---

## Architecture Decisions

| Decision | Choice | Why |
|---|---|---|
| Orchestration | Raw API calls | Avoids LangGraph abstraction overhead for MVP |
| Models | Llama 3.3 70B + 3.1 8B | Heavy model for reasoning, light for retrieval |
| Streaming | Server-Sent Events | Simpler than WebSockets, Vercel-native |
| State | Stateless per query | Clean, scalable, no session complexity |

---

## Tech Stack

**Backend**
- Python + FastAPI
- Groq API (Llama 3.3 70B / 3.1 8B)
- Server-Sent Events for streaming

**Frontend**
- React + Vite
- Vanilla CSS-in-JS (no UI library)
- Real-time agent panel updates

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Free [Groq API key](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/agentx.git
cd agentx
```

### 2. Set up the backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install groq fastapi uvicorn python-dotenv

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
```

### 3. Set up the frontend

```bash
cd ../frontend
npm install
```

### 4. Run

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

---

## Project Structure

```
agentx/
├── backend/
│   ├── main.py          # Agent logic + prompts
│   ├── server.py        # FastAPI + SSE streaming
│   └── .env             # GROQ_API_KEY (git ignored)
│
└── frontend/
    └── src/
        └── App.jsx      # UI + real-time agent panels
```

---

## Roadmap

- [ ] Parallel agent execution
- [ ] Web search tool integration (real-time data)
- [ ] Agent memory across sessions
- [ ] Router pattern — dynamic agent selection based on query type
- [ ] Export research as PDF/Markdown
- [ ] Production deployment on Vercel + Railway

---

## What I Learned

Building this taught me the core tradeoffs in multi-agent system design:

- **Orchestrator vs parallel execution** — sequential gives each agent full context from prior agents; parallel is faster but blind
- **Model selection per role** — using a heavier model only where reasoning depth matters cuts cost significantly  
- **Transparency as a feature** — showing agent reasoning builds more user trust than just showing the final answer
- **Critic pattern** — adversarial agents consistently surface blind spots that single-agent setups miss

---

## License

MIT
