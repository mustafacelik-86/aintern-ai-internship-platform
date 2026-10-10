"""
AIntern — API Route: Simulation Generation
POST /api/v1/generate
"""

from fastapi import APIRouter, HTTPException
from app.schemas.business_input import BusinessInput
from app.schemas.simulation import GenerateSimulationResponse
from app.services.simulation_generator import generate_simulation

router = APIRouter()


@router.post("/generate", response_model=GenerateSimulationResponse)
async def generate(input_data: BusinessInput):
    """
    Generate a company-specific internship simulation.

    - Accepts business/job listing context
    - Uses LLM to produce a unique simulation with tasks and rubrics
    - Saves to Supabase (company upsert + simulation insert) and returns the full object
    """
    try:
        simulation = await generate_simulation(input_data)

        return GenerateSimulationResponse(
            success=True,
            simulation_id=simulation.simulation_id,
            simulation=simulation,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
