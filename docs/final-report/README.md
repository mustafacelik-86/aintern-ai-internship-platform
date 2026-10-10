# AIntern - Final Project Overview & Testing Report



## 1. Project Overview



AIntern is an AI-powered internship simulation system designed to generate realistic internship tasks and evaluate candidate responses.



The project combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), FastAPI, ChromaDB, and Supabase to create internship simulations based on company information and then evaluate candidate performance.



During the internship, I worked through the main components of the system step by step, starting with basic LLM interaction and progressing to RAG, API/database integration, and finally the candidate evaluation and ranking pipeline.



## 2. Architecture and Technologies



The main technologies used in the project were:



- Python

- FastAPI

- Groq LLM API

- LangChain

- ChromaDB

- Supabase / PostgreSQL

- Pydantic

- Uvicorn

- Git and GitHub



The general system flow is:



Company Data → RAG Context → LLM → Internship Simulation → Candidate Responses → LLM Evaluation → Supabase → Candidate Ranking



## 3. Development Overview



### LLM Basics



The first stage focused on understanding how to interact with an LLM through an API. I tested system and user prompts, temperature settings, structured JSON output, and LangChain-based model calls.



This stage helped establish the basic LLM interaction used throughout the rest of the project.



### Retrieval-Augmented Generation (RAG)



The next stage introduced RAG using ChromaDB. Company information was stored as embeddings and retrieved according to a user query.



The retrieved company context was then supplied to the LLM when generating responses. Testing also demonstrated an important limitation of semantic retrieval: conceptually similar queries can sometimes retrieve unexpected documents.



### API and Database Integration



FastAPI and Supabase were integrated into the system to support simulation generation and persistence.



The `/api/v1/generate` endpoint was tested through Swagger. Generated simulations were successfully returned by the API and stored in the Supabase `simulations` table.



This connected the LLM generation pipeline with persistent application data.



### Candidate Evaluation Pipeline



The final development stage focused on evaluating candidate responses.



The `/api/v1/evaluate` endpoint uses an LLM-as-a-Judge approach. Candidate responses are evaluated against task-specific rubrics and the system produces:



- Task-level scores

- Grades

- Skills demonstrated

- Strengths and weaknesses

- Evidence

- Recommendations

- Overall score

- Skill profile

- Hiring recommendation



The ranking endpoint then retrieves evaluations for the same simulation and orders candidates by their overall score.



## 4. Testing and Results



The system was tested through Swagger and Supabase during development.



### Simulation Generation Test



The `/api/v1/generate` endpoint successfully returned HTTP 200 responses and generated internship simulations. The generated simulation was also successfully persisted in Supabase.



### Evaluation Test



The `/api/v1/evaluate` endpoint was tested with multiple candidate response sets for the same simulation.



Two candidates with different response quality were evaluated:



| Candidate | Overall Score | Grade | Hire Recommendation |

|---|---:|---|---|

| candidate_test_02 | 92 | Excellent | Strong Yes |

| candidate_test_01 | 68 | Adequate | Maybe |



The difference between the scores showed that the evaluation pipeline was able to distinguish between stronger and weaker candidate responses.



### Ranking Test



The ranking endpoint was tested using both candidates.



The returned ranking was:



1. candidate_test_02 - 92 - Strong Yes

2. candidate_test_01 - 68 - Maybe



The API returned `total: 2` and correctly sorted the candidates by overall score.



### Database Persistence Test



Evaluation results were verified directly in Supabase. Candidate IDs, simulation IDs, task scores, aggregate results, overall scores, and hiring recommendations were successfully persisted.



## 5. Issue Found and Fixed



During evaluation testing, the API successfully generated an evaluation but initially failed to save it to Supabase.



The database returned a foreign key error because the test `candidate_id` did not yet exist in the `candidates` table.



To resolve this, a candidate upsert step was added before saving an evaluation. This ensures that the candidate exists before the evaluation record is inserted.



After the fix:



- `/evaluate` returned HTTP 200

- No Supabase persistence warning occurred

- The candidate was available in the database

- The evaluation was successfully stored

- The stored evaluation appeared correctly in the ranking endpoint



This test was useful because it identified an integration issue that was not visible from the LLM evaluation result alone.



## 6. What I Learned



This project gave me practical experience with building an AI application as a complete pipeline rather than only making individual LLM calls.



The main areas I worked with were:



- Prompt engineering and structured LLM output

- LLM temperature and response behavior

- LangChain

- RAG and vector databases

- Embeddings and semantic retrieval

- FastAPI endpoints

- Pydantic schemas

- Supabase/PostgreSQL integration

- LLM-as-a-Judge evaluation

- Rubric-based scoring

- Candidate ranking

- API and database debugging

- Git branching and pull request workflow



One of the most important lessons was that a successful LLM response does not necessarily mean the complete application workflow is successful. Testing the API, database persistence, and downstream ranking together was necessary to verify the full system.



## 7. Conclusion



The AIntern project progressed from basic LLM experimentation to a working AI internship simulation and candidate evaluation pipeline.



By the end of the project, the system could generate internship simulations, store them in Supabase, evaluate candidate responses using task-specific criteria, persist evaluation results, and rank multiple candidates.



The final testing also identified and resolved a database integration issue, helping make the evaluation workflow more reliable.

## 8. Test Evidence

Supporting screenshots from the final evaluation tests are available in `docs/week5/`:

- `swagger-evaluate.png` - Successful `/evaluate` response
- `supabase-evaluations.png` - Evaluation persisted in Supabase
- `swagger-rankings-1.png` - Highest-ranked candidate result
- `swagger-rankings-2.png` - Second candidate and total ranking count

Additional evaluation and database integration evidence is available in `docs/week5/`.



