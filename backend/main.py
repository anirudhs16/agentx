from groq import Groq
import json

from dotenv import load_dotenv
load_dotenv()  # Load GROQ_API_KEY from .env

client = Groq()  # uses GROQ_API_KEY from env

# ── Agent prompts ──────────────────────────────────────
SUPERVISOR_PROMPT = """
You are a Supervisor orchestrating three specialist agents.
Your job: given a research question, decide what each agent 
should focus on, then synthesise their outputs into a final 
verdict with a confidence score (0-100).
Be explicit about your reasoning at every step.
"""

SEARCHER_PROMPT = """
You are a Searcher agent. Given a research question, find and 
list the most relevant raw facts, data points, and evidence. 
Be factual. No opinions. Just evidence.
"""

SYNTHESISER_PROMPT = """
You are a Synthesiser agent. Given raw evidence from the 
Searcher, build a clear, structured answer. Identify patterns. 
Draw conclusions. Be decisive.
"""

CRITIC_PROMPT = """
You are a Critic agent. Given the Synthesiser's answer, 
aggressively challenge it. Find holes, assumptions, missing 
evidence, and counterarguments. Be harsh but fair.
"""

VERDICT_PROMPT = """
You are a Supervisor delivering a FINAL VERDICT.
You have already received outputs from three specialist agents.
Do NOT create new agents. Do NOT assign new tasks.
Your only job: synthesise what you've received and deliver:
1. The final answer
2. Confidence score (0-100)
3. What the Critic got right
4. Your overall conclusion
Be decisive. One paragraph max per section.
"""

# ── Individual agent call ──────────────────────────────
def run_agent(system_prompt: str, user_message: str, 
              model: str = "llama-3.3-70b-versatile") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content

# ── Main orchestration loop ────────────────────────────
def run_synapse(query: str) -> dict:
    results = {}

    # Step 1: Supervisor plans
    print("🧠 Supervisor planning...")
    supervisor_plan = run_agent(
        SUPERVISOR_PROMPT,
        f"Research question: {query}\nCreate a focused task for each agent."
    )
    results["supervisor_plan"] = supervisor_plan

    # Step 2: Searcher finds evidence
    print("🔍 Searcher working...")
    search_output = run_agent(
        SEARCHER_PROMPT,
        f"Question: {query}\nSupervisor guidance: {supervisor_plan}",
        model="llama-3.1-8b-instant"  # lighter model for search
    )
    results["searcher"] = search_output

    # Step 3: Synthesiser builds answer
    print("⚡ Synthesiser working...")
    synthesis = run_agent(
        SYNTHESISER_PROMPT,
        f"Question: {query}\nEvidence: {search_output}"
    )
    results["synthesiser"] = synthesis

    # Step 4: Critic challenges it
    print("🔥 Critic working...")
    critique = run_agent(
        CRITIC_PROMPT,
        f"Answer to critique: {synthesis}",
        model="llama-3.1-8b-instant"
    )
    results["critic"] = critique

    # Step 5: Supervisor final verdict
    print("✅ Supervisor delivering verdict...")
    verdict = run_agent(
        SUPERVISOR_PROMPT,
        f"""Query: {query}
Searcher found: {search_output}
Synthesiser concluded: {synthesis}  
Critic challenged: {critique}

Now deliver your FINAL VERDICT. Include:
1. The answer
2. Confidence score (0-100)
3. Why you trust/distrust the synthesis
4. What the critic got right"""
    )
    results["verdict"] = verdict

    return results

# ── Run it ─────────────────────────────────────────────
if __name__ == "__main__":
    query = "Should a mid-level React developer switch to AI engineering in 2026?"
    output = run_synapse(query)
    
    for agent, response in output.items():
        print(f"\n{'='*50}")
        print(f"[{agent.upper()}]")
        print(response)