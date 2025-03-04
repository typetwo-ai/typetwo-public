from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig
from task_description import ORCHESTRATOR_INSTRUCTION
from database_schema import DATABASE_SCHEMA
from typing import Any

def generate_instructions_with_orchestrator(user_question: str) -> tuple[Any, str]:
    """Generates text instructions for other agents using the Orchestrator agent.

    Args:
        user_question (str): The question provided by the user.
    
    Returns:
        tuple[GenerateContentResponse, str]: The full response object and the extracted text response.
    
    References:
        https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#non-stream-multi-modality
    """
    prompt: str = f"User question:\n{user_question}\n\n{ORCHESTRATOR_INSTRUCTION}\n\n{DATABASE_SCHEMA}"
    model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(prompt)])
        ],
        generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
    )
    text_response: str = response.candidates[0].content.parts[0].text
    return response, text_response