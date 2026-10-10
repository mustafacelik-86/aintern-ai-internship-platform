"""
AIntern — Prompt Templates
All prompts live here so they're easy to iterate on without touching service logic.
"""

from langchain_core.prompts import ChatPromptTemplate


# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION GENERATION PROMPT
# ─────────────────────────────────────────────────────────────────────────────

SIMULATION_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at designing realistic, fair, and engaging internship skill assessments.

Your job is to create a simulation for a company that tests a candidate's relevant skills
through practical tasks — NOT generic trivia or abstract puzzles.

The simulation must:
- Feel like working at THIS specific company (use their tools, terminology, context)
- Be completable in the given time limit
- Have 3–5 distinct tasks of varying types (analytical, written, technical, etc.)
- Each task must have a clear success rubric

You MUST output valid JSON only. No markdown, no explanation outside the JSON.
""",
        ),
        (
            "human",
            """Create an internship simulation for the following company and position.

COMPANY INFORMATION:
- Name: {company_name}
- Industry: {industry}
- Position: {position}
- Job Description: {job_description}
- Tools Used: {tools_used}
- Project Context: {project_context}
- Desired Skills: {desired_skills}
- Total Simulation Duration: {simulation_duration_minutes} minutes

OUTPUT FORMAT (strict JSON):
{{
  "company_context": "2-3 sentence intro the candidate reads before starting",
  "scenario": "The overarching scenario/situation the candidate is placed in",
  "tasks": [
    {{
      "id": "task_1",
      "type": "analytical | written | technical | collaborative",
      "title": "Short task title",
      "description": "Full task description the candidate sees",
      "expected_skills": ["skill1", "skill2"],
      "rubric": "What a strong answer looks like",
      "time_limit_minutes": 15
    }}
  ],
  "evaluation_criteria": {{
    "must_haves": ["criterion1", "criterion2"],
    "good_to_haves": ["criterion1"],
    "red_flags": ["thing that would fail a candidate"]
  }}
}}
""",
        ),
    ]
)


# ─────────────────────────────────────────────────────────────────────────────
# CANDIDATE EVALUATION PROMPT
# ─────────────────────────────────────────────────────────────────────────────

CANDIDATE_EVALUATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a fair, evidence-based assessor evaluating internship candidates.

Your job is to score a candidate's response to a specific task based on a given rubric.
Be honest, specific, and constructive. Back every score with evidence from the response.

You MUST output valid JSON only. No markdown, no explanation outside the JSON.
""",
        ),
        (
            "human",
            """Evaluate the following candidate response.

TASK:
Title: {task_title}
Description: {task_description}
Rubric (what a strong answer looks like): {rubric}
Expected Skills: {expected_skills}

CANDIDATE RESPONSE:
{candidate_response}

OUTPUT FORMAT (strict JSON):
{{
  "score": <integer 0-100>,
  "grade": "Excellent | Good | Adequate | Poor",
  "skills_demonstrated": ["skill1", "skill2"],
  "strengths": ["specific strength from the response"],
  "weaknesses": ["specific gap or missed opportunity"],
  "evidence": "Quote or paraphrase from the response that supports your score",
  "recommendation": "Short hiring recommendation for this task"
}}
""",
        ),
    ]
)


# ─────────────────────────────────────────────────────────────────────────────
# AGGREGATE RANKING PROMPT
# ─────────────────────────────────────────────────────────────────────────────

CANDIDATE_RANKING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a hiring advisor summarizing multiple task scores into a final candidate assessment.
You MUST output valid JSON only.
""",
        ),
        (
            "human",
            """Summarize this candidate's overall performance across all tasks.

POSITION: {position}
DESIRED SKILLS: {desired_skills}

TASK SCORES:
{task_scores_json}

OUTPUT FORMAT (strict JSON):
{{
  "overall_score": <integer 0-100>,
  "overall_grade": "Excellent | Good | Adequate | Poor",
  "top_strengths": ["strength1", "strength2", "strength3"],
  "development_areas": ["area1", "area2"],
  "skill_profile": {{"skill_name": <0-10 score>}},
  "hire_recommendation": "Strong Yes | Yes | Maybe | No",
  "summary": "2-3 sentence overall narrative for the hiring manager"
}}
""",
        ),
    ]
)
