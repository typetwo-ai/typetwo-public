from vertexai.preview.generative_models import GenerativeModel, Content, Tool, FunctionDeclaration, ToolConfig, Part
from task_description import PROMPT_0_INSTRUCTION, PROMPT_1_INSTRUCTION, PROMPT_4_INSTRUCTION
from database_schema import DATABASE_SCHEMA, PROTEIN_MAPPING, GUIDE
from db_service import execute_query
import time


def db_search(search_instruction: str) -> str:
    """
    Searches the database and returns string results.

    Args:
        search_instruction: The search query string to execute.

    Returns:
        String containing the search results.
    """
    search_results = "5 cars" if search_instruction else None
    return search_results

def create_db_tool():
   
    db_search_func = FunctionDeclaration(
        name="db_search",
        description="Searches the database and returns string results.",
        parameters={
            "type": "object",
            "properties": {
                "search_instruction": {
                    "type": "string",
                    "description": "The search query string to execute."
                }
            },
            "required": ["search_instruction"]
        },
        response={
            "type": "object",
            "properties": {
                "result": {
                    "type": "string",
                    "description": "String containing the search results."
                }
            }
        }
    )


    db_tool = Tool(function_declarations=[db_search_func])
    return db_tool

def generate_instructions_with_orchestrator(user_question):
    prompt: str = f"User question:\n{user_question}\n\n{PROMPT_0_INSTRUCTION}\n\n{DATABASE_SCHEMA}"
    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(prompt)])
        ]
    )
    text_response = response.candidates[0].content.parts[0].text
    return response, text_response


def generate_sql_with_writer(user_question: str, writer_input: str, previous_query: str, previous_query_result: list[dict] | str) -> str:
    prompt: str = f"{PROMPT_1_INSTRUCTION}\n\n{DATABASE_SCHEMA}\n\nUser question:\n{user_question}\n\nOrchestrator input:\n{writer_input}\n\nPrevious sql query:\n{previous_query}\n\nPrevious query result:{previous_query_result}"
    model = GenerativeModel(model_name="gemini-2.0-flash-exp")
    exececute_query_tool = create_execute_query_tool()
    response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            tools=[exececute_query_tool],
            tool_config=ToolConfig(
                function_calling_config=ToolConfig.FunctionCallingConfig(mode=ToolConfig.FunctionCallingConfig.Mode.ANY)
            )
        )
    function_call = response.candidates[0].function_calls[0]
    sql_query: str = function_call.args["query"]
    return response, sql_query

def create_execute_query_tool():
    execute_query_func = FunctionDeclaration(
        name="execute_query",
        description="Executes a SQL query on BigQuery and returns the results as a list of records or an error message.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query string to execute on BigQuery."
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

def evaluate_query_with_checker(user_question, writer_input, checker_input):
    prompt: str = f"{PROMPT_4_INSTRUCTION}\n\n{DATABASE_SCHEMA}\n\n{GUIDE}\n\nQuery Result:\n{checker_input}\n\nOriginal user question:\n{user_question}\n\nWriter input:\n{writer_input}"
    model = GenerativeModel(model_name="gemini-1.5-flash-001")
    traffic_light_tool = create_traffic_light_tool()
    response = model.generate_content(
            contents=[
                Content(role="user", parts=[Part.from_text(prompt)])
            ],
            tools=[traffic_light_tool],
            tool_config=ToolConfig(
                function_calling_config=ToolConfig.FunctionCallingConfig(mode=ToolConfig.FunctionCallingConfig.Mode.ANY)
            )
        )
    function_call = response.candidates[0].function_calls[0]
    color: str = function_call.args["color"]
    return response, color

def create_traffic_light_tool():
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

def db_agent_loop(user_question, writer_input, sql_query, query_result, depth, max_depth):
    print(f"--- Depth: {depth} ---")
    if depth >= max_depth:
        return None, [{"error": "Max retries reached. Unable to generate a valid query."}]
    
    writer_response, sql_query = generate_sql_with_writer(user_question, writer_input, sql_query, query_result)
    print(sql_query)

    query_result = execute_query(sql_query)
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
