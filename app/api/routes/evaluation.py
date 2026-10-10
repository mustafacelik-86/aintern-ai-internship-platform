"""
AIntern — API Route: Candidate Evaluation
POST /api/v1/evaluate
GET  /api/v1/rankings/{simulation_id}
"""

from fastapi import APIRouter, HTTPException
from app.schemas.evaluation import EvaluateRequest, EvaluateResponse
from app.services.candidate_evaluator import evaluate_candidate
from app.services.supabase_client import (
    save_evaluation,
    get_simulation,
    get_rankings,
    upsert_candidate,
)
from app.schemas.simulation import Simulation

router = APIRouter()


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest):
    """
    Evaluate a candidate's simulation responses.

    - Fetches the original simulation from DB
    - Scores each task response using LLM-as-Judge
    - Generates aggregate score and hire recommendation
    - Saves and returns the full evaluation result
    """
    try:
        # Fetch the simulation to get task rubrics
        sim_data = await get_simulation(request.simulation_id)
        if not sim_data:
            raise HTTPException(
                status_code=404,
                detail=f"Simulation '{request.simulation_id}' not found",
            )

        simulation = Simulation(**sim_data)
        result = await evaluate_candidate(request, simulation)

        # Save to DB
        try:
            await upsert_candidate(request.candidate_id)
            await save_evaluation(result)
        except Exception as db_err:
            print(f"[WARN] Supabase save failed (continuing anyway): {db_err}")

        return EvaluateResponse(
            success=True,
            evaluation_id=result.evaluation_id,
            result=result,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rankings/{simulation_id}", tags=["Evaluation"])
async def rankings(simulation_id: str):
    """
    Get all candidate scores for a simulation, ranked highest to lowest.
    Business dashboard uses this to compare candidates.
    """
    try:
        data = await get_rankings(simulation_id)
        return {"simulation_id": simulation_id, "rankings": data, "total": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
