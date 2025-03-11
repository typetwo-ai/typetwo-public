from pathlib import Path
import numpy as np
import faiss
import pickle
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig
from backend.rag.agent_state import AgentState
from backend.rag.nodes.base_node import BaseNode


class ContextFilter(BaseNode):
    def __init__(self, data_folder: str = '/home/alex/typetwo-public/backend/rag/data', k: int = 5):
        self.data_folder = data_folder
        self.retriever = FAISSRetriever(data_folder=self.data_folder)
        self.k = k

    def __call__(self, state: AgentState) -> AgentState:
        original_question = state["original_question"]
        rephrased_question = state["rephrased_question"]
        model = GenerativeModel(model_name="gemini-2.0-flash-001")

        new_contexts = []

        for context in tqdm(state.get('retrieved_context'), desc='Filtering context'):
            file_name = Path('/home/alex/typetwo-public/backend/rag/data/parsed') / Path(context['metadata']['source'])
            content = open(file_name).read()
            prompt = f"""
               You are a document relevance evaluator. Your task is to determine if the provided document contains information relevant to answering the user's question.

               Answer ONLY with "yes" if the document contains information that would help answer the question.
               Answer ONLY with "no" if the document is not relevant to the question.

               Document content:
               {content}

               User question:
               {original_question}

               Is this document relevant to answering the user's question? (yes/no)
               """

            response = model.generate_content(
                contents=[
                    Content(role="user", parts=[Part.from_text(prompt)])
                ],
                generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
            )

            response_text = response.text.strip().lower()

            if response_text == 'yes':
                new_contexts.append(context)

        return {**state, "filtered_context": new_contexts}


class FAISSRetriever:
    def __init__(self, data_folder, model_name='microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract'):
        self.data_folder = Path(data_folder)
        self.embedder = SentenceTransformer(model_name)

        self.index_path = self.data_folder / 'preprocessed_data.index'
        self.metadata_path = self.data_folder / 'preprocessed_data.pkl'

        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError(f"FAISS index or metadata file not found in {self.data_folder}")

        self.index = faiss.read_index(str(self.index_path))

        with open(self.metadata_path, 'rb') as f:
            data = pickle.load(f)

        self.chunks = data.get('chunks', [])
        self.metadata = data.get('metadata', [])

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.encode([query])[0].reshape(1, -1).astype('float32')
        query_embedding /= np.linalg.norm(query_embedding, axis=1, keepdims=True)
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.chunks):
                results.append({
                    "content": self.chunks[idx],
                    "metadata": self.metadata[idx],
                    "score": float(distances[0][i])
                })

        return results
