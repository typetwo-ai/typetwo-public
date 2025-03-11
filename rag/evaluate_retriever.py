import itertools
import json
import os

import faiss
import pandas as pd
import torch
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from tqdm import tqdm


def score(retrieved_nodes, expected_doc, expected_page):
    for idx, node in enumerate(retrieved_nodes):
        source = node.metadata.get("file_name", "Unknown")

        if source == expected_doc:
            return idx, True

    return -1, False


def save_retrieval_results(model_name, chunk_size, chunk_overlap, qa_pair, retrieved_nodes, target_found, position):
    results_dir = f"retrieval_results/{model_name}/cs{chunk_size}_co{chunk_overlap}"
    os.makedirs(results_dir, exist_ok=True)

    question_slug = qa_pair['question'].lower().replace(" ", "_")[:30]
    output_file = f"{results_dir}/{question_slug}.json"

    retrieval_results = []

    for idx, node in enumerate(retrieved_nodes):
        result = {
            "position": idx,
            "text": node.text,
            "score": node.score if hasattr(node, 'score') else None,
            "file_name": node.metadata.get("file_name", "Unknown"),
            "page": node.metadata.get("page", "Unknown")
        }

        if node.metadata.get("file_name") == qa_pair['document']:
            result["target"] = True

        retrieval_results.append(result)

    output_data = {
        "question": qa_pair['question'],
        "expected_document": qa_pair['document'],
        "expected_page": qa_pair['page'],
        "target_found": target_found,
        "target_position": position if target_found else -1,
        "retrieved_nodes": retrieval_results
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)


def evaluate_retrieval_single(
        model_config,
        questions_answers,
        chunk_size,
        chunk_overlap,
        data_dir="data/parsed",
        top_k=30
):
    model_name = model_config['name']
    model_path = model_config['model_name']

    print(f"Evaluating model: {model_name} with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")

    embed_model = HuggingFaceEmbedding(
        model_name=model_path,
        trust_remote_code=True
    )
    Settings.embed_model = embed_model
    embed_dim = len(embed_model.get_text_embedding("Sample text for dimension detection"))

    # Settings.node_parser = SentenceSplitter(
    #     chunk_size=chunk_size,
    #     chunk_overlap=chunk_overlap,
    # )
    Settings.node_parser = MarkdownNodeParser()

    documents = SimpleDirectoryReader(
        data_dir,
        required_exts=[".md"],
        recursive=True
    ).load_data()

    faiss_index = faiss.IndexFlatIP(embed_dim)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    retriever = index.as_retriever(similarity_top_k=top_k)

    position_scores = []
    first_positions = []

    for qa_pair in questions_answers:
        question = qa_pair['question']
        expected_doc = qa_pair['document']
        expected_page = qa_pair['page']

        retrieved_nodes = retriever.retrieve(question)

        position, target_found = score(retrieved_nodes, expected_doc, expected_page)

        if target_found:
            position_scores.append(-position)  # Negative for ranking (higher is better)
            first_positions.append(position)
        else:
            position_scores.append(-top_k - 1)  # Worse than the last position
            first_positions.append(-1)

        save_retrieval_results(
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            qa_pair=qa_pair,
            retrieved_nodes=retrieved_nodes,
            target_found=target_found,
            position=position
        )

    mean_position_score = sum(position_scores) / len(position_scores) if position_scores else 0

    print(f"Mean Position Score for {model_name} (cs={chunk_size}, co={chunk_overlap}): {mean_position_score:.4f}")

    del embed_model
    del faiss_index
    del vector_store
    del index
    del retriever

    return model_name, chunk_size, chunk_overlap, mean_position_score, first_positions


def run_all_evaluations(models, questions_answers, chunking_configs, output_file="evaluation_summary.csv"):
    all_results = []

    for model_config, chunk_config in tqdm(itertools.product(models, chunking_configs),
                                           total=len(models) * len(chunking_configs)):
        result = evaluate_retrieval_single(
            model_config=model_config,
            questions_answers=questions_answers,
            chunk_size=chunk_config['chunk_size'],
            chunk_overlap=chunk_config['chunk_overlap']
        )

        result_dict = {
            'model': result[0],
            'chunk_size': result[1],
            'chunk_overlap': result[2],
            'position_score': result[3],
            'first_positions': result[4],
            'total_questions': len(questions_answers)
        }

        all_results.append(result_dict)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    summary_df = pd.DataFrame(all_results)
    summary_df.to_csv(output_file, index=False)

    print("\nEvaluation Summary (sorted by position score):")
    print(summary_df.sort_values(by=['position_score'], ascending=False).to_string(index=False))

    return summary_df


if __name__ == "__main__":
    models = [
        {
            'name': 'granite-embedding-107m-multilingual',
            'model_name': 'ibm-granite/granite-embedding-107m-multilingual',
        },
        {
            'name': 'BiomedNLP-BiomedBERT-base-uncased-abstract',
            'model_name': 'microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract',
        },
        {
            'name': 'biobert-base-cased-v1.2',
            'model_name': 'dmis-lab/biobert-base-cased-v1.2',
        },
        {
            'name': 'pubmedbert-base-embeddings',
            'model_name': 'NeuML/pubmedbert-base-embeddings-matryoshka',
        },
    ]

    questions_answers = [
        {
            'question': 'I am trying to optimise potency and pk of a part of my molecule that has methoxybenzene',
            'document': '0095-0107.md',
            'page': '4'
        },
        {
            'question': 'how does anti - HCC mechanism of platinum complexes work?',
            'document': '0001-0017.md',
            'page': '4'
        }
    ]

    chunking_configs = [
        {'chunk_size': 128, 'chunk_overlap': 15},
        # {'chunk_size': 256, 'chunk_overlap': 20},
        # {'chunk_size': 512, 'chunk_overlap': 20},
        # {'chunk_size': 1024, 'chunk_overlap': 50},
        # {'chunk_size': 2048, 'chunk_overlap': 100}
    ]

    summary = run_all_evaluations(models, questions_answers, chunking_configs)
