from io import BytesIO
import logging
from google.cloud import storage
from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig
from typing import Any
import json
from tqdm import tqdm
import os

from task_description import PDF_ANALYSIS_INSTRUCTION

logger = logging.getLogger(__name__)

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["title", "keywords"]
}

RESPONSE_SCHEMA_2 = {
    "type": "object",
    "properties": {
        "documents": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["documents"]
}

def generate_answer(prompt: str) -> str:
    _, documents = retrieve_relevant_documents(prompt)
    documents: list = json.loads(documents)["documents"]
    print(documents)
    _, answer = ask_gemini(prompt, documents)
    print(answer)
    return answer

def ask_gemini(prompt: str, documents: list) -> tuple[Any, str]:
    try:
        data_part = [Part.from_uri(uri=document, mime_type="application/pdf") for document in documents]
        prompt = f"Instructions: {PDF_ANALYSIS_INSTRUCTION}\n\nUser input: {prompt}"
        model = GenerativeModel(model_name="gemini-2.0-flash-001")
        response = model.generate_content(
            contents=[
                Content(role="user", parts=[*data_part, Part.from_text(prompt)])
            ],
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )
        
        text_response: str = response.candidates[0].content.parts[0].text
        
        return response, text_response
    except Exception as e:
        logger.exception(f"Error querying Gemini with documents: {str(e)}")
        raise Exception(f"Failed to get response from Gemini: {str(e)}")

def retrieve_relevant_documents(prompt: str) -> tuple[Any, json]:
    with open("index.json", "r", encoding="utf-8") as file:
        json_content = json.load(file)
    json_text = json.dumps(json_content)
    
    prompt = f"Go throgh the keywords and select the 5 to 10 most relevant documents based on the user input. User input:\n{prompt}\n\n{json_text}"
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(prompt)])
        ],
        generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1, response_mime_type="application/json", response_schema=RESPONSE_SCHEMA_2)
    )
    documents = response.candidates[0].content.parts[0].text
    return response, documents


def generate_keywords(file_path: str):
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    prompt = "Generate a list of 100 high value and specific keywords for the following document. The output should be a json with title and keywords. For abbreviations, use the abbreviaion and the full form as a single keyword. Make sure that the keywords are compatible with json parsing. Again, make sure you don't use any symbols incompatible with json. Use only standard characters. Don't use weird characters."
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_uri(uri=file_path, mime_type="application/pdf"), Part.from_text(prompt)])
        ],
        generation_config=GenerationConfig(response_mime_type="application/json", response_schema=RESPONSE_SCHEMA)
    )
    keywords = response.candidates[0].content.parts[0].text
    return response, keywords

def build_index(documents: list):
    index = {}
    if os.path.exists("index.json"):
        with open("index.json", "r") as f:
            index = json.load(f)
    
    for document in tqdm(documents, desc="Processing Documents"):
        if document not in index:
            print(f"Adding new document: {document}")
            _, keywords = generate_keywords(document)
            keywords = json.loads(keywords)
            index[document] = {
                "title": keywords["title"],
                "keywords": keywords["keywords"]
            }
            json.dump(index, open("index.json", "w"), indent=4)
        else:
            print(f"Skipping already processed document: {document}")
    
    print(f"Index built and saved to index.json")
    return index

def get_document_paths(prefix="Journal of Medicinal Chemistry"):
    bucket_name = "literature-resources-bucket"
    client = storage.Client()

    blobs = client.list_blobs(bucket_name, prefix=prefix)
    documents = [f"gs://{bucket_name}/{blob.name}" for blob in blobs if blob.name.endswith('.pdf')]
    
    return documents

if __name__ == "__main__":

    prompt = "I'm working on protacs and want to evaluate degradation kinetics."
       
    try:
        print("Starting...")
        # print(prompt)
        documents = get_document_paths()
        print(documents)
        # _, answer = ask_gemini(prompt, documents)
        # print(answer)
        # response, keywords = generate_keywords(document_1)
        # print(keywords)
        index = build_index(documents)
        # _, documents = retrieve_relevant_documents(prompt)
        # print(documents)
        # answer = generate_answer(prompt)
        # print(answer)
        

    except Exception as e:
        print(f"Error during testing: {str(e)}")