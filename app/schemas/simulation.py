"""
AIntern — Pydantic Schemas: Simulation
Defines the shape of a generated simulation and its tasks.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SimulationTask(BaseModel):
    id: str
    type: str  # analytical | written | technical | collaborative
    title: str
    description: str
    expected_skills: List[str]
    rubric: str
    time_limit_minutes: int


class EvaluationCriteria(BaseModel):
    must_haves: List[str]
    good_to_haves: List[str]
    red_flags: List[str]


class Simulation(BaseModel):
    """The full simulation object returned by /generate and stored in Supabase."""

    simulation_id: str
    company_id: str
    company_name: str
    position: str
    company_context: str
    scenario: str
    tasks: List[SimulationTask]
    evaluation_criteria: EvaluationCriteria
    simulation_duration_minutes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GenerateSimulationResponse(BaseModel):
    """API response wrapper for POST /generate."""

    success: bool
    simulation_id: str
    simulation: Simulation
    message: str = "Simulation generated successfully"
