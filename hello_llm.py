from app.core.llm import get_llm

llm = get_llm(temperature=0.3)

response = llm.invoke(
    "What is an internship simulation? Answer in 3 short bullet points."
)

print(response.content)