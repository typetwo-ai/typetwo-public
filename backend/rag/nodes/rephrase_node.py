from backend.rag.agent_state import AgentState
from backend.rag.nodes.base_node import BaseNode
from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig


class QuestionRephraser(BaseNode):
    def __init__(self, model_name: str = "gemini-pro", temperature: float = 0.2):
        self.model_name = model_name
        self.temperature = temperature

    def __call__(self, state: AgentState) -> AgentState:
        """Rephrase the original question to improve retrieval"""
        question = state["original_question"]

        model = GenerativeModel(model_name="gemini-2.0-flash-001")

        prompt = f"""
        You are an expert at reformulating user queries to make them more effective for retrieval. 
        Your task is to rephrase the user's question to make it more specific and searchable.
        Do not add information that is not in the original question.
        Return only the rephrased question without any additional text. 
        
        The question:
        
        {question}
        """

        response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )

        rephrased = response.text.strip()

        return {"original_question": question, "rephrased_question": rephrased}