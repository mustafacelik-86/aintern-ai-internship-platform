"""
AIntern — Simulation Generator Service
Core business logic for generating a company-specific simulation via LLM.
"""

import json
import uuid
from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser

from app.core.llm import get_llm, strip_think_tags
from app.core.prompts import SIMULATION_GENERATION_PROMPT
from app.core.vector_store import upsert_company_context
from app.config import settings
from app.services.supabase_client import upsert_company, save_simulation
from app.schemas.business_input import BusinessInput
from app.schemas.simulation import (
    Simulation,
    SimulationTask,
    EvaluationCriteria,
)


def _build_context_text(input_data: BusinessInput) -> str:
    """Create a single text blob from business input for embedding."""
    return (
        f"Company: {input_data.company_name}. "
        f"Industry: {input_data.industry}. "
        f"Position: {input_data.position}. "
        f"Description: {input_data.job_description}. "
        f"Tools: {', '.join(input_data.tools_used)}. "
        f"Context: {input_data.project_context}. "
        f"Skills: {', '.join(input_data.desired_skills)}."
    )


async def generate_simulation(input_data: BusinessInput) -> Simulation:
    """
    Main function: take business input → call LLM → return a Simulation object.

    Steps:
    1. Embed company context into ChromaDB (for future RAG use)
    2. Build the LangChain prompt
    3. Call Groq LLM, parse JSON response
    4. Validate and return Simulation object
    """

    # ── Step 1: Embed company context ────────────────────────────────────────
    company_id = input_data.company_id or str(uuid.uuid4())
    context_text = _build_context_text(input_data)

    upsert_company_context(
        company_id=company_id,
        company_name=input_data.company_name,
        context_text=context_text,
    )

    # ── Step 2 & 3: Build chain and call LLM ─────────────────────────────────
    llm = get_llm(temperature=0.75)  # Some creativity for varied simulations
    chain = (
        SIMULATION_GENERATION_PROMPT
        | llm
        | (lambda msg: msg.content)
        | (lambda text: strip_think_tags(text))
        | JsonOutputParser()
    )

    raw = await chain.ainvoke(
        {
            "company_name": input_data.company_name,
            "industry": input_data.industry,
            "position": input_data.position,
            "job_description": input_data.job_description,
            "tools_used": ", ".join(input_data.tools_used),
            "project_context": input_data.project_context,
            "desired_skills": ", ".join(input_data.desired_skills),
            "simulation_duration_minutes": input_data.simulation_duration_minutes,
        }
    )

    # ── Step 4: Map raw LLM dict → validated Simulation object ───────────────
    simulation_id = str(uuid.uuid4())

    tasks = [
        SimulationTask(
            id=task.get("id", f"task_{i+1}"),
            type=task.get("type", "analytical"),
            title=task["title"],
            description=task["description"],
            expected_skills=task.get("expected_skills", []),
            rubric=task.get("rubric", ""),
            time_limit_minutes=task.get("time_limit_minutes", 15),
        )
        for i, task in enumerate(raw["tasks"])
    ]

    criteria_raw = raw.get("evaluation_criteria", {})
    evaluation_criteria = EvaluationCriteria(
        must_haves=criteria_raw.get("must_haves", []),
        good_to_haves=criteria_raw.get("good_to_haves", []),
        red_flags=criteria_raw.get("red_flags", []),
    )

    simulation = Simulation(
        simulation_id=simulation_id,
        company_id=company_id,
        company_name=input_data.company_name,
        position=input_data.position,
        company_context=raw["company_context"],
        scenario=raw["scenario"],
        tasks=tasks,
        evaluation_criteria=evaluation_criteria,
        simulation_duration_minutes=input_data.simulation_duration_minutes,
        created_at=datetime.utcnow(),
    )

    # ── Step 5: Persist to Supabase ───────────────────────────────────────────
    # Company must exist before simulation due to FK constraint
    if settings.supabase_url and settings.supabase_anon_key:
        await upsert_company(
            company_id=company_id,
            company_name=input_data.company_name,
            industry=input_data.industry,
        )
        await save_simulation(simulation)

    return simulation
