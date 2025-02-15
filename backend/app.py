from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.auth
import logging

from db_agent import generate_instructions_with_orchestrator, db_agent_loop

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
        
        return jsonify({
            'figure': None,
            'search_results': query_result if query_result else []
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)