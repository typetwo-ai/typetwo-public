from vertexai.preview.generative_models import GenerativeModel, Content, Tool, FunctionDeclaration, ToolConfig, Part, GenerationConfig
from task_description import WRITER_INSTRUCTION, CHECKER_INSTRUCTION, EXAMPLES
from database_schema import DATABASE_SCHEMA, TABLES
from utils import execute_query
from typing import Any


def db_agent_loop(user_question: str, writer_input: str, sql_query: str, query_result: list[dict] | str, depth: int, max_depth: int):
    """Runs a recursive database agent loop to execute and refine SQL queries.

    Allows the Writer and Checker agents to interact. If the initial query fails or produces inadequate results, the loop allows
    for iterative Writer-Checker correction to ultimately generate the desired SQL. A maximum depth prevents infinite recursion.

    Args:
        user_question (str): The question provided by the user.
        writer_input (str): The input provided to the Writer agent from the Orchestrator agent.
        sql_query (str): The SQL query to execute.
        query_result (list[dict] | str): The results or error from the SQL query.
        depth (int): The current depth of the recursive loop.
        max_depth (int): The maximum depth allowed for the recursive loop.

    Returns:
        If successful, the final SQL query and the results of the query.
    """
    print(f"--- Depth: {depth} ---")
    if depth >= max_depth:
        return None, [{"error": "Max retries reached. Unable to generate a valid query."}]
    
    writer_response, sql_query = generate_sql_with_writer(user_question, writer_input, sql_query, query_result)
    print(sql_query)

    query_result = execute_query(sql_query, limit=100)
    print(query_result)

    checker_response, traffic_light = evaluate_query_with_checker(user_question, writer_input, query_result)
    print(f"Traffic light: {traffic_light}")
    
    if traffic_light == "green":
        return sql_query, query_result
    elif traffic_light == "red":
        depth += 1
        return db_agent_loop(user_question, writer_input, sql_query, query_result, depth, max_depth)
    else:
        return sql_query, [{"error": "Traffic light is neither green or red"}]


def generate_sql_with_writer(user_question: str, writer_input: str, previous_query: str, previous_query_result: list[dict] | str) -> str:
    """Generates mysql code using the Writer agent. It is designed to operate in a loop with the Checker agent.

    Args:
        user_question (str): The question provided by the user.
        writer_input (str): The input provided to the Writer agent from the Orchestrator agent.
        previous_query (str): SQL of the previous query executed (if any).
        previous_query_result (list[dict] | str): The results or error from the previous query (if any).
    
    Returns:
        str: SQL code generated by the Writer agent.
    
    References:
        https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/function-calling
    """
    prompt: str = f"{WRITER_INSTRUCTION}\n\n{DATABASE_SCHEMA, TABLES}\n\nUser question:\n{user_question}\n\nOrchestrator input:\n{writer_input}\n\nExamples:\n{EXAMPLES}\n\nPrevious sql query:\n{previous_query}\n\nPrevious query result:{previous_query_result}"
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    exececute_query_tool = create_execute_query_tool()
    response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            tools=[exececute_query_tool],
            tool_config=ToolConfig(
                function_calling_config=ToolConfig.FunctionCallingConfig(mode=ToolConfig.FunctionCallingConfig.Mode.ANY)
            ),
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )
    function_call = response.candidates[0].function_calls[0]
    sql_query: str = function_call.args["query"]
    return response, sql_query


def create_execute_query_tool():
    """Creates a tool that allows the Writer agent to use function calling to generate the sql code.
    
    Returns:
        Tool objcet that can be called by the Writer agent.
    """
    execute_query_func = FunctionDeclaration(
        name="execute_query",
        description="Executes a SQL query on Cloud SQL and returns the results as a list of records or an error message.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query string to execute on Cloud SQL."
                }
            },
            "required": ["query"]
        },
        response={
            "type": "object",
            "properties": {
                "result": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "description": "A list of records retrieved from the database, with each record as a key-value dictionary."
                    }
                },
                "error": {
                    "type": "string",
                    "description": "Error message if query execution fails. If successful, this field is empty or null."
                }
            }
        }
    )
    execute_query_tool = Tool(function_declarations=[execute_query_func])
    return execute_query_tool

def evaluate_query_with_checker(user_question: str, writer_input: str, checker_input:str) -> tuple[Any, str]:
    """Evaluates the results of the SQL query using the Checker agent. It is designed to operate in a loop with the Writer agent.

    Args:
        user_question (str): The question provided by the user.
        writer_input (str): The input provided to the Writer agent from the Orchestrator agent.
        checker_input (str): The results or the error from the SQL query to evaluate.
    
    Returns:
        tuple[GenerateContentResponse, str]: The full response object and the traffic light color (green: results good, red: results bad).
    
    References:
        https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/function-calling
    """
    prompt: str = f"{CHECKER_INSTRUCTION}\n\n{DATABASE_SCHEMA}\n\nQuery Result:\n{checker_input}\n\nOriginal user question:\n{user_question}\n\nWriter input:\n{writer_input}"
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    traffic_light_tool = create_traffic_light_tool()
    response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            tools=[traffic_light_tool],
            tool_config=ToolConfig(
                function_calling_config=ToolConfig.FunctionCallingConfig(mode=ToolConfig.FunctionCallingConfig.Mode.ANY)
            ),
            generation_config=GenerationConfig(temperature=0, top_k=1, top_p=1)
        )
    function_call = response.candidates[0].function_calls[0]
    color: str = function_call.args["color"]
    return response, color

def create_traffic_light_tool():
   """Creates a tool that allows the Checker agent to use function calling to set the trafic light to green or red.
    
    Returns:
        Tool objcet that can be called by the Checker agent.
    """
   traffic_light_func = FunctionDeclaration(
       name="set_traffic_light",
       description="Sets the traffic light color based on query result satisfaction. Green indicates satisfactory results, red indicates unsatisfactory or incomplete results.",
       parameters={
           "type": "object",
           "properties": {
               "color": {
                   "type": "string",
                   "enum": ["green", "red"],
                   "description": "The color to set the traffic light to. Green for satisfactory results, red for unsatisfactory."
               }
           },
           "required": ["color"]
       }
   )
   traffic_light_tool = Tool(function_declarations=[traffic_light_func])
   return traffic_light_tool