from vertexai.preview.generative_models import GenerativeModel, Content, Part
from task_description import ORCHESTRATOR_INSTRUCTION
from database_schema import DATABASE_SCHEMA

def generate_instructions_with_orchestrator(user_question):
    prompt: str = f"User question:\n{user_question}\n\n{ORCHESTRATOR_INSTRUCTION}\n\n{DATABASE_SCHEMA}"
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(prompt)])
        ]
    )
    text_response = response.candidates[0].content.parts[0].text
    return response, text_response