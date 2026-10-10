"""
AIntern — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import simulation, evaluation

app = FastAPI(
    title="AIntern API",
    description="AI-powered internship simulation engine",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(simulation.router, prefix="/api/v1", tags=["Simulation"])
app.include_router(evaluation.router, prefix="/api/v1", tags=["Evaluation"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AIntern API is running 🚀"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
