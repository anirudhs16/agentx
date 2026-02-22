import { useState } from "react"

const agents = [
  { key: "searcher", label: "Searcher", icon: "🔍", 
    desc: "Finding evidence" },
  { key: "synthesiser", label: "Synthesiser", icon: "⚡", 
    desc: "Building answer" },
  { key: "critic", label: "Critic", icon: "🔥", 
    desc: "Challenging assumptions" },
  { key: "verdict", label: "Verdict", icon: "✅", 
    desc: "Final judgement" },
]

export default function App() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState({})
  const [active, setActive] = useState(null)
  const [loading, setLoading] = useState(false)

  const runResearch = async () => {
    if (!query.trim()) return
    setResults({})
    setLoading(true)

    const res = await fetch("http://localhost:8000/research", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split("\n").filter(l => l.startsWith("data:"))

      for (const line of lines) {
        const data = JSON.parse(line.replace("data: ", ""))
        setActive(data.agent)
        setResults(prev => ({ ...prev, [data.agent]: data.content }))
      }
    }

    setActive(null)
    setLoading(false)
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      color: "#e5e5e5",
      fontFamily: "'Inter', sans-serif",
      padding: "40px 24px"
    }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 48 }}>
        <h1 style={{ fontSize: 32, fontWeight: 700, 
          color: "#fff", margin: 0 }}>
          Synapse
        </h1>
        <p style={{ color: "#666", marginTop: 8, fontSize: 14 }}>
          Multi-agent research. Watch them think.
        </p>
      </div>

      {/* Query Input */}
      <div style={{ 
        maxWidth: 640, margin: "0 auto 48px",
        display: "flex", gap: 12 
      }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && runResearch()}
          placeholder="Ask anything worth researching..."
          style={{
            flex: 1, padding: "14px 18px",
            background: "#111", border: "1px solid #222",
            borderRadius: 10, color: "#fff", fontSize: 15,
            outline: "none"
          }}
        />
        <button
          onClick={runResearch}
          disabled={loading}
          style={{
            padding: "14px 24px",
            background: loading ? "#222" : "#fff",
            color: loading ? "#666" : "#000",
            border: "none", borderRadius: 10,
            fontWeight: 600, cursor: loading ? "default" : "pointer",
            fontSize: 15, transition: "all 0.2s"
          }}
        >
          {loading ? "Running..." : "Research"}
        </button>
      </div>

      {/* Agent Panels */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
        gap: 16, maxWidth: 1200, margin: "0 auto"
      }}>
        {agents.map(agent => (
          <div key={agent.key} style={{
            background: "#111",
            border: `1px solid ${active === agent.key ? "#444" : "#1a1a1a"}`,
            borderRadius: 12, padding: 20,
            transition: "border-color 0.3s",
            opacity: loading && !results[agent.key] && 
              active !== agent.key ? 0.4 : 1
          }}>
            {/* Agent Header */}
            <div style={{ 
              display: "flex", alignItems: "center", 
              gap: 10, marginBottom: 16 
            }}>
              <span style={{ fontSize: 20 }}>{agent.icon}</span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 14 }}>
                  {agent.label}
                </div>
                <div style={{ color: "#555", fontSize: 12 }}>
                  {agent.desc}
                </div>
              </div>
              {active === agent.key && (
                <div style={{
                  marginLeft: "auto", width: 8, height: 8,
                  borderRadius: "50%", background: "#4ade80",
                  animation: "pulse 1s infinite"
                }} />
              )}
            </div>

            {/* Agent Output */}
            <div style={{
              fontSize: 13, lineHeight: 1.7, color: "#aaa",
              minHeight: 120,
              whiteSpace: "pre-wrap", wordBreak: "break-word"
            }}>
              {results[agent.key] || (
                <span style={{ color: "#333" }}>
                  {loading ? "Waiting..." : "Run a query to see output"}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
        * { box-sizing: border-box; }
      `}</style>
    </div>
  )
}