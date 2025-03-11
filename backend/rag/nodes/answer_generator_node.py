from pathlib import Path

from backend.rag.agent_state import AgentState
from backend.rag.nodes.base_node import BaseNode
from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig


class AnswerGenerator(BaseNode):
    def __init__(self, model_name: str = "gemini-pro", temperature: float = 0.3):
        self.model_name = model_name
        self.temperature = temperature

    def __call__(self, state: AgentState) -> AgentState:
        question = state["original_question"]
        context = state["filtered_context"]

        formatted_context = ""
        for i, doc in enumerate(context):
            file_name = Path('/home/alex/typetwo-public/backend/rag/data/parsed') / Path(context[i]['metadata']['source'])
            content = open(file_name).read()
            formatted_context += f"Document #{i + 1}:\n"
            formatted_context += f"Content: {content}\n\n"

        model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")

        prompt = f"""
        You are a helpful assistant. Use the provided context to answer the user's question.
        Be specific and provide details from the context when possible. 
        If the context doesn't contain information to answer the question, say "I don't have enough information to answer this question."
        Cite the source documents when appropriate.
        
        <context>
        {formatted_context}
        </context>
        
        Question:
        
        {question}
        """

        response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )

        answer = response.text.strip()

        return {**state, "answer": answer}
