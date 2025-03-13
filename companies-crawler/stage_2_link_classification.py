import glob
import json
import os
import time
from pathlib import Path

import google.auth
from tqdm.auto import tqdm
from vertexai.preview.generative_models import GenerativeModel, Content, Tool, FunctionDeclaration, ToolConfig, Part, \
    GenerationConfig

credentials, project = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = "project-1-450712"


is_useful_schema = {
    "type": "object",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "Explanation for why you made this determination"
        },
        "is_useful": {
            "type": "boolean",
            "description": "Indicates whether the link contains the information i am interested in"
        }
    },
    "required": ["reasoning", "is_useful"]
}


def load_json_files(links_dir: str):
    all_data = {}
    for file_path in glob.glob(os.path.join(links_dir, "*.json")):
        filename = os.path.basename(file_path).replace('.json', '')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_data[filename] = data
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return all_data


model = GenerativeModel(
    # "gemini-2.0-pro-exp-02-05"
    "gemini-2.0-flash-exp"
)


def handle_company(company_name, data, folder, filename, with_reasoning=True):
    links = data['links']

    dir_path = Path(folder)
    dir_path.mkdir(parents=True, exist_ok=True)

    output_path = dir_path / Path(filename)

    link2result = {}

    counter = 0
    for link in tqdm(links, desc=f'Handling links for company {company_name}'):

        if counter != 0 and counter % 10 == 0:  # remove it if you dont use free exp model
            time.sleep(61)

        counter += 1

        prompt = \
        f"""
        I have a biotech/chemistry company called {company_name} with website {data['start_url']}. 
        I will give you a link that was found by recursively crawling through their website.

        Your task is to analyze this link and classify whether it contains valuable information about the company's research and achievements. Specifically:

        1. Determine if this link contains substantive content such as: research papers, press releases, news articles, scientific publications, case studies, product information, or innovation announcements.

        2. Provide a brief assessment of the content type and its relevance to understanding the company's scientific work and capabilities.

        IMPORTANT NOTES:
        - All links provided come from crawling the company's website domain or are explicitly linked from their website
        - If you see a link from a different domain (e.g., a partner organization, journal, or news site), still check it out for any useful info i am interested in
        - Focus on scientific/research content rather than general company information like "About Us" or contact pages
        - I am not interested in employers of the company

        The link to analyze: {link}
        """

        response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            tools=[
                Tool(
                    function_declarations=[
                        FunctionDeclaration(
                            name="is_useful",
                            description="Classify if this link contains the information i am interested in",
                            parameters=is_useful_schema
                        )
                    ]
                )
            ],
            tool_config=ToolConfig(
                function_calling_config=ToolConfig.FunctionCallingConfig(mode=ToolConfig.FunctionCallingConfig.Mode.ANY)
            ),
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )

        args = response.candidates[0].function_calls[0].args
        is_useful = args['is_useful']
        reasoning = args['reasoning']

        link2result[link] = {
            'cls': 'useful' if is_useful else 'other',
            'reasoning': reasoning
        }

        save_result(data, link2result, output_path, with_reasoning=with_reasoning)


def save_result(initial_data, link2result, output_path, with_reasoning=False):
    initial_data['links'] = []
    for link, result in link2result.items():
        item = {
            'link': link,
            'cls': result['cls'],
            'reasoning': result['reasoning']
        }

        if not with_reasoning:
            del item['reasoning']

        initial_data['links'].append(item)

    with open(output_path, "w") as f:
        f.write(json.dumps(initial_data, indent=4))


if __name__ == "__main__":
    company2data = load_json_files('website_links')
    for item in company2data.items():
        company_name = item[0]
        data = item[1]
        handle_company(company_name, data, './classified_links', company_name + '.json')
