from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.agents import router as agents_router
from app.api.routes.projects import router as projects_router

app = FastAPI(
    title="Bedrock AI Addon Orchestrator",
    version="0.4.0",
    description="Plataforma com orquestração multiagente para criação e revisão de addons Bedrock.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router, prefix="/api")
app.include_router(agents_router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "bedrock-ai-addon-orchestrator",
        "version": "0.4.0",
    }
