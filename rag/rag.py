import os
from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class RAGRetrieval:
    """
    A configurable retrieval component for RAG pipelines with fine-grained control over each step.
    Uses LangChain for document loading and chunking, with granite-embedding-107m-multilingual for embeddings.
    Modified to work with TXT files instead of PDFs.
    """

    def __init__(
            self,
            txt_directory: str,
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
            embedding_model_name: str = "ibm-granite/granite-embedding-107m-multilingual"
    ):
        self.txt_directory = txt_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model_name

        self.documents = []
        self.chunks = []
        self.vectorstore = None
        self.embeddings = None

    def load_documents(self) -> List[Document]:
        print(f"Loading TXT documents from {self.txt_directory}")

        loader = DirectoryLoader(
            self.txt_directory,
            glob="**/*.txt",
            loader_cls=TextLoader
        )

        self.documents = loader.load()
        print(f"Loaded {len(self.documents)} documents")

        return self.documents

    def chunk_documents(
            self,
            chunk_size: Optional[int] = None,
            chunk_overlap: Optional[int] = None
    ) -> List[Document]:
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents() first.")

        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap

        print(f"Chunking documents with size={chunk_size}, overlap={chunk_overlap}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,  # Track the start index of each chunk
        )

        self.chunks = text_splitter.split_documents(self.documents)
        print(f"Created {len(self.chunks)} chunks")

        return self.chunks

    def initialize_embeddings(self, model_name: Optional[str] = None) -> None:
        model_name = model_name or self.embedding_model_name
        print(f"Initializing embeddings with model: {model_name}")

        # Create HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cuda" if os.environ.get("USE_CUDA", "0") == "1" else "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

    def create_vectorstore(self) -> FAISS:
        if not self.chunks:
            raise ValueError("No chunks available. Call chunk_documents() first.")

        if not self.embeddings:
            self.initialize_embeddings()

        print("Creating vector store...")

        self.vectorstore = FAISS.from_documents(
            self.chunks,
            self.embeddings
        )

        print("Vector store created successfully")
        return self.vectorstore

    def save_vectorstore(self, path: str) -> None:
        if not self.vectorstore:
            raise ValueError("No vector store available. Call create_vectorstore() first.")

        print(f"Saving vector store to {path}")
        self.vectorstore.save_local(path)

    def load_vectorstore(self, path: str) -> FAISS:
        if not self.embeddings:
            self.initialize_embeddings()

        print(f"Loading vector store from {path}")
        self.vectorstore = FAISS.load_local(path, self.embeddings, )
        return self.vectorstore

    def retrieve(self, query: str, k: int = 10, score_threshold: Optional[float] = None) -> List[Document]:
        if not self.vectorstore:
            raise ValueError("No vector store available. Call create_vectorstore() first.")

        print(f"Retrieving top {k} chunks for query: '{query}'")

        docs_and_scores = self.vectorstore.similarity_search_with_score(query, k=k)

        if score_threshold is not None:
            docs_and_scores = [(doc, score) for doc, score in docs_and_scores if score >= score_threshold]

        retrieved_docs = []
        for doc, score in docs_and_scores:
            doc.metadata["similarity_score"] = float(score)
            retrieved_docs.append(doc)

        print(f"Retrieved {len(retrieved_docs)} chunks")
        return retrieved_docs


# Example usage
if __name__ == "__main__":
    # Initialize the retrieval pipeline
    retriever = RAGRetrieval(
        txt_directory="/Users/alex/typetwo-public/rag/data/parsed",
        chunk_size=500,
        chunk_overlap=50
    )

    # Process the documents
    retriever.load_documents()
    retriever.chunk_documents()
    retriever.initialize_embeddings()
    retriever.create_vectorstore()

    # Optional: Save the vector store for later use
    retriever.save_vectorstore("./vectorstore")

    # Retrieve chunks for a query
    query = "chemistry"
    retrieved_chunks = retriever.retrieve(query, k=10)

    # Print retrieved chunks with their metadata
    for i, chunk in enumerate(retrieved_chunks):
        print(f"\nChunk {i + 1}:")
        print(f"Content: {chunk.page_content[:150]}...")
        print(f"Source: {chunk.metadata.get('source', 'Unknown')}")
        print(f"Similarity Score: {chunk.metadata.get('similarity_score', 'Unknown')}")