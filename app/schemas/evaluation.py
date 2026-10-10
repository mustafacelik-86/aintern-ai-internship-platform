"""
AIntern — Pydantic Schemas: Evaluation
Defines the shape of candidate evaluation requests and results.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class TaskResponse(BaseModel):
    """A single candidate response to one task."""
    task_id: str
    response: str = Field(..., min_length=10)


class EvaluateRequest(BaseModel):
    """Request body for POST /evaluate."""
    simulation_id: str
    candidate_id: str
    task_responses: List[TaskResponse]


class TaskScore(BaseModel):
    """Score for a single task."""
    task_id: str
    task_title: str
    score: int = Field(..., ge=0, le=100)
    grade: str  # Excellent | Good | Adequate | Poor
    skills_demonstrated: List[str]
    strengths: List[str]
    weaknesses: List[str]
    evidence: str
    recommendation: str


class AggregateResult(BaseModel):
    """Overall candidate result across all tasks."""
    overall_score: int = Field(..., ge=0, le=100)
    overall_grade: str
    top_strengths: List[str]
    development_areas: List[str]
    skill_profile: Dict[str, int]  # {"Python": 8, "Communication": 6}
    hire_recommendation: str  # Strong Yes | Yes | Maybe | No
    summary: str


class EvaluationResult(BaseModel):
    """Full evaluation result stored in Supabase and returned by /evaluate."""
    evaluation_id: str
    simulation_id: str
    candidate_id: str
    task_scores: List[TaskScore]
    aggregate: AggregateResult
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class EvaluateResponse(BaseModel):
    """API response wrapper for POST /evaluate."""
    success: bool
    evaluation_id: str
    result: EvaluationResult
    message: str = "Evaluation completed successfully"
