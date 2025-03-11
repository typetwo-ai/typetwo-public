import os
from typing import Dict, Any

from backend.rag.nodes.answer_generator_node import AnswerGenerator
from backend.rag.nodes.context_filter_node import ContextFilter
from backend.rag.nodes.context_retrieve_node import ContextRetriever
from backend.rag.nodes.rephrase_node import QuestionRephraser
import langgraph.graph as lg
from langgraph.graph import END
from langgraph.checkpoint.memory import MemorySaver


os.environ["GOOGLE_CLOUD_PROJECT"] = "project-1-450712"


class RAGAgent:
    def __init__(self,
                 data_folder: str = '/home/alex/typetwo-public/backend/rag/data',
                 question_model: str = "gemini-pro",
                 answer_model: str = "gemini-pro"):
        self.question_rephraser = QuestionRephraser(model_name=question_model)
        self.context_retriever = ContextRetriever(data_folder=data_folder, k=10)
        self.context_filter = ContextFilter(data_folder=data_folder, k=10)
        self.answer_generator = AnswerGenerator(model_name=answer_model)

        self.graph = self._create_graph()

    def _create_graph(self):
        builder = lg.Graph()

        builder.add_node("rephrase_question", self.question_rephraser)
        builder.add_node("retrieve_context", self.context_retriever)
        builder.add_node("filter_context", self.context_filter)
        builder.add_node("generate_answer", self.answer_generator)

        builder.add_edge("rephrase_question", "retrieve_context")
        builder.add_edge("retrieve_context", "filter_context")
        builder.add_edge("filter_context", "generate_answer")
        builder.add_edge("generate_answer", END)

        builder.set_entry_point("rephrase_question")

        return builder.compile()

    def run(self, question: str) -> Dict[str, Any]:
        memory = MemorySaver()

        result = self.graph.invoke(
            {"original_question": question},
            config={"checkpointer": memory}
        )

        return result


agent = RAGAgent()

# print(agent.run("how does anti-HCC mechanism of platinum complexes work?"))
print(agent.run("I am trying to optimise potency and pk of a part of my molecule that has methoxybenzene. Suggest me what i can do."))
