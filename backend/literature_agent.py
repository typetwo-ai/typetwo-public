from io import BytesIO
import logging
from google.cloud import storage
from vertexai.preview.generative_models import GenerativeModel, Content, Part, GenerationConfig
from typing import Any
import json

logger = logging.getLogger(__name__)

def ask_gemini(prompt: str, documents: list) -> tuple[Any, str]:
    try:
        data_part = [Part.from_uri(uri=document, mime_type="application/pdf") for document in documents]

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

def retrieve_document_list(prompt: str) -> list:
    return documents

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["title", "keywords"]
}

def generate_keywords(file_path: str):
    model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
    prompt = "Generate a list of 100 high value and specific keywords for the following document. The output should be a json with title and keywords. For abbreviations, use the abbreviaion and the full form as a single keyword."
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_uri(uri=file_path, mime_type="application/pdf"), Part.from_text(prompt)])
        ],
        generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1, response_mime_type="application/json", response_schema=RESPONSE_SCHEMA)
    )
    keywords = response.candidates[0].content.parts[0].text
    return response, keywords

def build_index(documents: list):
    index = {}
    for document in documents:
        _, keywords = generate_keywords(document)
        keywords = json.loads(keywords)
        index[document] = {
            "title": keywords["title"],
            "keywords": keywords["keywords"]
        }
    return index

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    document_1 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0001-0017.pdf"
    document_2 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0018-0048.pdf"
    document_3 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0049-0080.pdf"
    document_4 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0081-0094.pdf"
    document_5 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0095-0107.pdf"
    document_6 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0108-0134.pdf"
    document_7 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0135-0155.pdf"
    document_8 = f"gs://literature-resources-bucket/Journal of Medicinal Chemistry/2025 Volume 68/01  (001-850)/0156-0173.pdf"

    documents = [document_1, document_2, document_3, document_4, document_5, document_6, document_7, document_8]
    prompt = "I'm working on immunotherapeutic in vivo assays? Is there anything I need to be aware of? Base your answer on the documents."
       
    try:
        # _, answer = ask_gemini(prompt, documents)
        # print(answer)
        # response, keywords = generate_keywords(document_1)
        # print(keywords)
        index = build_index(documents)
        print(index)
        json.dump(index, open("index.json", "w"), indent=4)
    except Exception as e:
        print(f"Error during testing: {str(e)}") 