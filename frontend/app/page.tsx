"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Project = {
  id: string;
  name: string;
  theme: string;
  style: string;
  fidelity: string;
  version: string;
  status: string;
};

type Agent = {
  id: string;
  name: string;
  role: string;
  responsibilities: string[];
};

export default function HomePage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [name, setName] = useState("Guardião do Eclipse");
  const [theme, setTheme] = useState("fantasia sombria com arte de espada lendária e criaturas místicas");
  const [style, setStyle] = useState("inspiracao-fiel");
  const [fidelity, setFidelity] = useState("high");
  const [loading, setLoading] = useState(false);

  async function loadProjects() {
    const response = await fetch(`${API_URL}/api/projects`);
    const data = await response.json();
    setProjects(data);
  }

  async function loadAgents() {
    const response = await fetch(`${API_URL}/api/agents`);
    const data = await response.json();
    setAgents(data);
  }

  useEffect(() => {
    loadProjects();
    loadAgents();
  }, []);

  async function handleCreateProject() {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          theme,
          style,
          fidelity,
          version: "0.0.1",
          target_platform: "bedrock-1.20+",
        }),
      });

      if (!response.ok) {
        throw new Error("Erro ao criar projeto");
      }

      await response.json();
      await loadProjects();
    } finally {
      setLoading(false);
    }
  }

  async function runAgentsForProject(projectId: string) {
    await fetch(`${API_URL}/api/agents/${projectId}/run`, {
      method: "POST",
    });
    await loadProjects();
  }

  return (
    <main style={{ minHeight: "100vh", background: "#06111f", color: "#edf6ff", fontFamily: "Arial, sans-serif" }}>
      <div style={{ maxWidth: 1280, margin: "0 auto", padding: 32 }}>
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28, gap: 16, flexWrap: "wrap" }}>
          <div>
            <div style={{ color: "#7dd3fc", letterSpacing: 2, fontSize: 12, textTransform: "uppercase" }}>Minecraft Bedrock</div>
            <h1 style={{ margin: "8px 0 0", fontSize: 42 }}>Bedrock AI Addon Orchestrator</h1>
          </div>
          <button
            style={{ background: "#38bdf8", color: "#06131b", border: "none", borderRadius: 12, padding: "12px 18px", fontWeight: 800 }}
            onClick={handleCreateProject}
            disabled={loading}
          >
            {loading ? "Gerando..." : "Novo projeto"}
          </button>
        </header>

        <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 18, marginBottom: 28 }}>
          {[
            ["Projetos", String(projects.length)],
            ["Agentes", String(agents.length)],
            ["Versões", "42"],
            ["Exports", "27"],
          ].map(([label, value]) => (
            <div key={label} style={{ background: "#101827", border: "1px solid #243244", borderRadius: 16, padding: 20 }}>
              <div style={{ color: "#94a3b8", fontSize: 13 }}>{label}</div>
              <div style={{ marginTop: 8, fontSize: 32, fontWeight: 800 }}>{value}</div>
            </div>
          ))}
        </section>

        <section style={{ display: "grid", gridTemplateColumns: "1.3fr 0.7fr", gap: 20 }}>
          <div style={{ background: "#111827", border: "1px solid #243244", borderRadius: 20, padding: 24 }}>
            <h2 style={{ marginTop: 0 }}>Criar projeto</h2>
            <div style={{ display: "grid", gap: 16 }}>
              <div>
                <label style={{ display: "block", marginBottom: 8, color: "#cbd5e1" }}>Nome do projeto</label>
                <input
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 10, padding: 12 }}
                />
              </div>

              <div>
                <label style={{ display: "block", marginBottom: 8, color: "#cbd5e1" }}>Tema / obra / inspiração</label>
                <input
                  value={theme}
                  onChange={(event) => setTheme(event.target.value)}
                  style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 10, padding: 12 }}
                />
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div>
                  <label style={{ display: "block", marginBottom: 8, color: "#cbd5e1" }}>Estilo</label>
                  <select
                    value={style}
                    onChange={(event) => setStyle(event.target.value)}
                    style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 10, padding: 12 }}
                  >
                    <option value="inspiracao-fiel">Inspiração fiel</option>
                    <option value="inspiracao-original">Inspiração + originalidade</option>
                    <option value="novo-estilo">Estilo original</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: "block", marginBottom: 8, color: "#cbd5e1" }}>Fidelidade</label>
                  <select
                    value={fidelity}
                    onChange={(event) => setFidelity(event.target.value)}
                    style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 10, padding: 12 }}
                  >
                    <option value="low">Baixa</option>
                    <option value="medium">Média</option>
                    <option value="high">Alta</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleCreateProject}
                style={{ background: "#22c55e", color: "#062b10", border: "none", padding: "14px 18px", borderRadius: 12, fontWeight: 800 }}
              >
                Gerar plano do addon
              </button>
            </div>
          </div>

          <aside style={{ background: "#111827", border: "1px solid #243244", borderRadius: 20, padding: 24 }}>
            <h2 style={{ marginTop: 0 }}>Agentes conectados</h2>
            <div style={{ display: "grid", gap: 12 }}>
              {agents.map((agent) => (
                <div key={agent.id} style={{ padding: "12px 14px", borderRadius: 12, background: "#0f172a", border: "1px solid #334155" }}>
                  <div style={{ fontWeight: 700 }}>{agent.name}</div>
                  <div style={{ color: "#cbd5e1", marginTop: 6 }}>{agent.role}</div>
                </div>
              ))}
            </div>
          </aside>
        </section>

        <section style={{ marginTop: 28, background: "#111827", border: "1px solid #243244", borderRadius: 20, padding: 24 }}>
          <h2 style={{ marginTop: 0 }}>Projetos</h2>

          {projects.length === 0 ? (
            <p style={{ margin: 0, color: "#cbd5e1" }}>Nenhum projeto ainda. Crie o primeiro para começar.</p>
          ) : (
            <div style={{ display: "grid", gap: 14 }}>
              {projects.map((project) => (
                <div key={project.id} style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 14, padding: 18 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                    <div>
                      <div style={{ fontSize: 22, fontWeight: 700 }}>{project.name}</div>
                      <div style={{ color: "#94a3b8", marginTop: 4 }}>{project.theme}</div>
                    </div>
                    <button
                      onClick={() => runAgentsForProject(project.id)}
                      style={{ background: "#f59e0b", color: "#1a1200", border: "none", borderRadius: 10, padding: "10px 14px", fontWeight: 700 }}
                    >
                      Executar agentes
                    </button>
                  </div>
                  <div style={{ marginTop: 10, color: "#cbd5e1" }}>
                    {project.style} · {project.fidelity} · {project.status}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
