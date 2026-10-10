"""
AIntern — Pydantic Schemas: Business Input
Defines the shape of data a business sends to request a simulation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class BusinessInput(BaseModel):
    """
    The payload a business (or the platform) sends to generate a simulation.
    All fields help the LLM understand the company's specific context.
    """

    company_name: str = Field(
        ...,
        description="Name of the company",
        examples=["Acme Corp"],
    )
    industry: str = Field(
        ...,
        description="Industry or sector",
        examples=["SaaS / B2B", "E-commerce", "Fintech"],
    )
    position: str = Field(
        ...,
        description="Position title being hired for",
        examples=["Software Engineering Intern", "Marketing Intern"],
    )
    job_description: str = Field(
        ...,
        description="Full or summarized job description",
        min_length=50,
    )
    tools_used: List[str] = Field(
        default_factory=list,
        description="Tools/software the team uses daily",
        examples=[["GitHub", "Jira", "Figma", "Slack"]],
    )
    project_context: str = Field(
        ...,
        description="Brief description of current projects or team focus",
        min_length=20,
    )
    desired_skills: List[str] = Field(
        default_factory=list,
        description="Key skills the ideal candidate should demonstrate",
        examples=[["Python", "data analysis", "communication"]],
    )
    simulation_duration_minutes: int = Field(
        default=45,
        description="Total expected time for the candidate to complete the simulation",
        ge=15,
        le=120,
    )
    company_id: Optional[str] = Field(
        default=None,
        description="Optional existing company ID (for repeat simulations)",
    )
