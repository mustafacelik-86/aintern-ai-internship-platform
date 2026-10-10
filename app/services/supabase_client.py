"""
AIntern — Supabase Client
Handles all database read/write operations.
"""

from supabase import create_client, Client
from app.config import settings
from app.schemas.simulation import Simulation
from app.schemas.evaluation import EvaluationResult
import json


def get_client() -> Client:
    """Return a Supabase client. Call this per-request (client is lightweight)."""
    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
    )


# ── Companies ─────────────────────────────────────────────────────────────────

async def upsert_company(company_id: str, company_name: str, industry: str = "") -> dict:
    """
    Insert company if it doesn't exist yet (upsert by company_id).
    Must be called before save_simulation() to satisfy the foreign key constraint.
    """
    client = get_client()
    data = {
        "company_id": company_id,
        "company_name": company_name,
        "industry": industry,
    }
    result = (
        client.table("companies")
        .upsert(data, on_conflict="company_id")
        .execute()
    )
    return result.data[0] if result.data else {}


# ── Simulations ───────────────────────────────────────────────────────────────

async def save_simulation(simulation: Simulation) -> dict:
    """Persist a generated simulation to Supabase."""
    client = get_client()
    data = {
        "simulation_id": simulation.simulation_id,
        "company_id": simulation.company_id,
        "company_name": simulation.company_name,
        "position": simulation.position,
        "company_context": simulation.company_context,
        "scenario": simulation.scenario,
        "tasks": json.loads(simulation.model_dump_json())["tasks"],
        "evaluation_criteria": json.loads(simulation.model_dump_json())["evaluation_criteria"],
        "simulation_duration_minutes": simulation.simulation_duration_minutes,
    }
    result = client.table("simulations").insert(data).execute()
    return result.data[0] if result.data else {}


async def get_simulation(simulation_id: str) -> dict | None:
    """Fetch a simulation by ID."""
    client = get_client()
    result = (
        client.table("simulations")
        .select("*")
        .eq("simulation_id", simulation_id)
        .single()
        .execute()
    )
    return result.data

# ── Candidates ────────────────────────────────────────────────────────────────

async def upsert_candidate(candidate_id: str) -> dict:
    """
    Insert candidate if it doesn't exist yet.
    Must be called before save_evaluation() to satisfy the foreign key constraint.
    """
    client = get_client()
    data = {
        "candidate_id": candidate_id,
    }
    result = (
        client.table("candidates")
        .upsert(data, on_conflict="candidate_id")
        .execute()
    )
    return result.data[0] if result.data else {}

# ── Evaluations ───────────────────────────────────────────────────────────────

async def save_evaluation(evaluation: EvaluationResult) -> dict:
    """Persist an evaluation result to Supabase."""
    client = get_client()
    data = {
        "evaluation_id": evaluation.evaluation_id,
        "simulation_id": evaluation.simulation_id,
        "candidate_id": evaluation.candidate_id,
        "task_scores": json.loads(evaluation.model_dump_json())["task_scores"],
        "aggregate": json.loads(evaluation.model_dump_json())["aggregate"],
        "overall_score": evaluation.aggregate.overall_score,
        "hire_recommendation": evaluation.aggregate.hire_recommendation,
    }
    result = client.table("evaluations").insert(data).execute()
    return result.data[0] if result.data else {}


async def get_rankings(simulation_id: str) -> list[dict]:
    """Get all candidates ranked by score for a given simulation."""
    client = get_client()
    result = (
        client.table("evaluations")
        .select("candidate_id, overall_score, hire_recommendation, aggregate")
        .eq("simulation_id", simulation_id)
        .order("overall_score", desc=True)
        .execute()
    )
    return result.data or []
