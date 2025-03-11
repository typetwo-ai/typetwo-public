from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import google.auth
import logging
import os
import uuid
from datetime import datetime
from io import BytesIO

import pandas as pd
from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS

from db_agent import db_agent_loop
from orch_agent import generate_instructions_with_orchestrator
from reporter_agent import generate_summary_with_reporter
from utils import execute_query
from literature_agent import generate_answer


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

request_id2sql = {}

credentials, project = google.auth.default()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Project ID: {project}")


@app.route("/api/health")
def health():
    return "OK", 200


@app.route('/api/query', methods=['OPTIONS'])
def options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/query', methods=['POST'])
def process_query():
    try:
        data = request.json
        user_question = data.get('query', '')
        logger.info(f"Received user query: {user_question}")

        orchestrator_response, writer_input = generate_instructions_with_orchestrator(user_question)
        logging.info(writer_input)

        sql_query, query_result = db_agent_loop(user_question, writer_input, sql_query="", query_result="", depth=0, max_depth=5)

        request_id = str(uuid.uuid4())

        request_id2sql[request_id] = sql_query

        reporter_response, answer_summary = generate_summary_with_reporter(user_question, writer_input, sql_query, query_result)
        logging.info(answer_summary)

        return jsonify({
            'requestId': request_id,
            'summary': answer_summary,
            'searchResults': query_result if query_result else []
        })

    except Exception as e:
        logger.exception("Error processing query")
        return jsonify({'error': str(e)}), 500


@app.post("/api/download-excel/<request_id>")
def download_excel(request_id: str):
    results = execute_query(request_id2sql[request_id], limit=10000000)
    try:
        df = pd.DataFrame(results)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Search Results', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Search Results']
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D3D3D3',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            for i, col in enumerate(df.columns):
                max_width = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(i, i, max_width)
        output.seek(0)

        filename = f"chembl35_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        import traceback
        from flask import make_response
        response = make_response(f"Error generating Excel file: {str(e)}\n{traceback.format_exc()}")
        response.status_code = 500
        return response

@app.route('/api/literature', methods=['POST'])
def process_query():
    data = request.get_json()
    answer = generate_answer(data)
    return jsonify({'summary': answer})

if __name__ == '__main__':
    app.run(debug=True)