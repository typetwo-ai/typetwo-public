from pathlib import Path
import numpy as np
import faiss
import pickle
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer

from backend.rag.agent_state import AgentState
from backend.rag.nodes.base_node import BaseNode


class ContextRetriever(BaseNode):
    def __init__(self, data_folder: str = '/home/alex/typetwo-public/backend/rag/data', k: int = 5):
        self.data_folder = data_folder
        self.retriever = FAISSRetriever(data_folder=self.data_folder)
        self.k = k

    def __call__(self, state: AgentState) -> AgentState:
        rephrased_question = state["rephrased_question"]

        results = self.retriever.retrieve(rephrased_question, k=self.k)

        return {**state, "retrieved_context": results}


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
