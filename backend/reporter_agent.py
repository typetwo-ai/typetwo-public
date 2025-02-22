from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig
from task_description import REPORTER_INSTRUCTION
from typing import Any

def generate_summary_with_reporter(user_question: str, orchestrator_response: str, sql_query: str, query_result: list[dict]) -> tuple[Any, str]:
    prompt: str = f"Instructions:\n{REPORTER_INSTRUCTION}\n\nUser question:\n{user_question}\n\nOrchestrator agent:\n{orchestrator_response}\n\nSql query:\n{sql_query}\n\nQuery result:\n{query_result}"
    model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(prompt)])
        ],
        generation_config=GenerationConfig(temperature=0)
    )
    text_response: str = response.candidates[0].content.parts[0].text

    return response, text_response