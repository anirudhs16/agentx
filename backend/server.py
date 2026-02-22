from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from main import run_agent, SEARCHER_PROMPT, SYNTHESISER_PROMPT, CRITIC_PROMPT, SUPERVISOR_PROMPT
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# Streams each agent result as it completes
async def stream_agents(query: str):
    agents = [
        ("searcher", SEARCHER_PROMPT, "llama-3.1-8b-instant"),
        ("synthesiser", SYNTHESISER_PROMPT, "llama-3.3-70b-versatile"),
        ("critic", CRITIC_PROMPT, "llama-3.1-8b-instant"),
        ("verdict", SUPERVISOR_PROMPT, "llama-3.3-70b-versatile"),
    ]

    for agent_name, prompt, model in agents:
        # Small delay so UI can show agents "thinking" sequentially
        await asyncio.sleep(0.5)
        
        result = run_agent(prompt, query, model)
        
        yield f"data: {json.dumps({'agent': agent_name, 'content': result})}\n\n"

@app.post("/research")
async def research(request: QueryRequest):
    return StreamingResponse(
        stream_agents(request.query),
        media_type="text/event-stream"
    )