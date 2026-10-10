"""
AIntern — Candidate Evaluator Service
Scores candidate responses using LLM-as-a-Judge pattern.
"""

import json
import uuid
from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser

from app.core.llm import get_llm
from app.core.prompts import (
    CANDIDATE_EVALUATION_PROMPT,
    CANDIDATE_RANKING_PROMPT,
)
from app.schemas.evaluation import (
    EvaluateRequest,
    EvaluationResult,
    TaskScore,
    AggregateResult,
)
from app.schemas.simulation import Simulation


async def evaluate_candidate(
    request: EvaluateRequest,
    simulation: Simulation,
) -> EvaluationResult:
    """
    Evaluate a candidate's responses against the simulation's tasks.

    Steps:
    1. For each task response → call LLM with rubric (LLM-as-Judge)
    2. Collect all task scores
    3. Call LLM again for aggregate summary + hire recommendation
    4. Return full EvaluationResult
    """

    llm = get_llm(temperature=0.2)  # Low temperature → consistent scoring
    eval_chain = CANDIDATE_EVALUATION_PROMPT | llm | JsonOutputParser()
    rank_chain = CANDIDATE_RANKING_PROMPT | llm | JsonOutputParser()

    # Build a lookup map: task_id → task object
    task_map = {task.id: task for task in simulation.tasks}

    # ── Step 1 & 2: Score each task ──────────────────────────────────────────
    task_scores: list[TaskScore] = []

    for task_response in request.task_responses:
        task = task_map.get(task_response.task_id)
        if task is None:
            continue  # Skip unknown task IDs

        raw_score = await eval_chain.ainvoke(
            {
                "task_title": task.title,
                "task_description": task.description,
                "rubric": task.rubric,
                "expected_skills": ", ".join(task.expected_skills),
                "candidate_response": task_response.response,
            }
        )

        task_scores.append(
            TaskScore(
                task_id=task.id,
                task_title=task.title,
                score=raw_score["score"],
                grade=raw_score["grade"],
                skills_demonstrated=raw_score.get("skills_demonstrated", []),
                strengths=raw_score.get("strengths", []),
                weaknesses=raw_score.get("weaknesses", []),
                evidence=raw_score.get("evidence", ""),
                recommendation=raw_score.get("recommendation", ""),
            )
        )

    # ── Step 3: Aggregate ─────────────────────────────────────────────────────
    task_scores_summary = [
        {
            "task_title": ts.task_title,
            "score": ts.score,
            "grade": ts.grade,
            "skills_demonstrated": ts.skills_demonstrated,
            "strengths": ts.strengths,
            "weaknesses": ts.weaknesses,
        }
        for ts in task_scores
    ]

    raw_aggregate = await rank_chain.ainvoke(
        {
            "position": simulation.position,
            "desired_skills": ", ".join(
                skill
                for task in simulation.tasks
                for skill in task.expected_skills
            ),
            "task_scores_json": json.dumps(task_scores_summary, indent=2),
        }
    )

    aggregate = AggregateResult(
        overall_score=raw_aggregate["overall_score"],
        overall_grade=raw_aggregate["overall_grade"],
        top_strengths=raw_aggregate.get("top_strengths", []),
        development_areas=raw_aggregate.get("development_areas", []),
        skill_profile=raw_aggregate.get("skill_profile", {}),
        hire_recommendation=raw_aggregate["hire_recommendation"],
        summary=raw_aggregate["summary"],
    )

    # ── Step 4: Return full result ────────────────────────────────────────────
    return EvaluationResult(
        evaluation_id=str(uuid.uuid4()),
        simulation_id=request.simulation_id,
        candidate_id=request.candidate_id,
        task_scores=task_scores,
        aggregate=aggregate,
        evaluated_at=datetime.utcnow(),
    )
