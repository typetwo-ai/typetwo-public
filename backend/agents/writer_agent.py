import logging
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.agent_state import AgentState
from backend.task_description import (
    WRITER_INSTRUCTION,
    EXAMPLES
)
from backend.utils import execute_query

from backend.agents.utils import get_model

logger = logging.getLogger(__name__)


def writer_agent(state: AgentState) -> AgentState:
    """
    Writer agent that generates SQL queries based on the Orchestrator's instructions.
    """
    logger.info(f"Running Writer agent (iteration {state.iteration_count + 1})")
    state.active_agent = "writer"
    state.iteration_count += 1

    # Format previous query results for display
    previous_results = "No previous results"
    if state.query_results:
        previous_results = str(state.query_results[:5])
    elif state.query_error:
        previous_results = f"Error: {state.query_error}"

    # Create the writer prompt
    writer_prompt = ChatPromptTemplate.from_template(WRITER_INSTRUCTION)

    # Run the model
    model = get_model("gemini-2.0-flash-001")
    chain = writer_prompt | model | StrOutputParser()

    # Execute the chain
    checker_feedback = ""
    if state.checker_feedback and state.iteration_count > 1:
        checker_feedback = f"Checker Feedback:\n{state.checker_feedback}"

    sql_query = chain.invoke({
        "writer_instruction": WRITER_INSTRUCTION,
        # "database_schema": DATABASE_SCHEMA,
        # "tables": TABLES,
        "examples": EXAMPLES,
        "user_question": state.user_question,
        "orchestrator_instructions": state.orchestrator_instructions,
        "iteration_count": state.iteration_count,
        "previous_query": state.sql_query,
        "previous_results": previous_results,
        "checker_feedback": checker_feedback
    })

    # Extract SQL query (in case the model included explanation despite instructions)
    sql_query = extract_sql_query(sql_query)

    # Execute the SQL query
    try:
        logger.info(f"Executing SQL query: {sql_query[:100]}...")
        query_results = execute_query(sql_query)
        state.query_results = query_results
        state.query_error = None
        logger.info(f"Query executed successfully. Got {len(query_results)} results")
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        state.query_results = []
        state.query_error = str(e)

    # Update state
    state.sql_query = sql_query

    return state


def extract_sql_query(text: str) -> str:
    """Extract SQL query from text that may contain markdown code blocks."""
    # Look for SQL between ```sql and ``` markers
    sql_pattern = r"```sql\s*(.*?)\s*```"
    matches = re.findall(sql_pattern, text, re.DOTALL)

    if matches:
        return matches[0].strip()

    # If no SQL code blocks found, try finding just code blocks
    code_pattern = r"```\s*(.*?)\s*```"
    matches = re.findall(code_pattern, text, re.DOTALL)

    if matches:
        return matches[0].strip()

    # Return the original text if no code blocks found
    return text.strip()