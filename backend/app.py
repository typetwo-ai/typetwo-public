from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.generativeai as genai
from db_service import execute_query
from task_description import PROMPT_1_INSTRUCTION, PROMPT_2_INSTRUCTION, PROMPT_3_INSTRUCTION
from database_schema import DATABASE_SCHEMA, PROTEIN_MAPPING, GUIDE
from utils import extract_sql_query, convert_numpy_arrays
from db_agent import create_db_tool, db_search, generate_sql_with_writer, generate_instructions_with_orchestrator, evaluate_query_with_checker, db_agent_loop
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from exec_debug import generate_figure
from vertexai.preview.generative_models import GenerativeModel, Content, Part, Tool, FunctionDeclaration, ToolConfig
import google.auth
import logging

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/api/health")
def health():
    return "OK", 200

credentials, project = google.auth.default()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Project ID: {project}")

@app.route('/api/query', methods=['OPTIONS'])
def options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/query', methods=['POST'])
def process_query() -> dict[str, list[tuple] | str]:
    try:
        data: dict = request.json
        user_question = data.get('query', '')
        logging.info(user_question)
        orchestrator_response, writer_input = generate_instructions_with_orchestrator(user_question)
        logging.info(writer_input)

        sql_query, query_result = db_agent_loop(user_question, writer_input, sql_query="", query_result="", depth=0, max_depth=5)
        logging.info(sql_query)
        logging.info(query_result)
        

        figure = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[3, 1, 2])])
        processed_figure = convert_numpy_arrays(figure.to_dict())
        figure = None
        
        return jsonify({
            'figure': processed_figure if figure else None,
            'search_results': query_result if query_result else []
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)