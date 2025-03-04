import logging
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.agent_state import AgentState
from backend.database_schema import DATABASE_SCHEMA
from backend.task_description import (
    CHECKER_INSTRUCTION
)

from backend.agents.utils import get_model

# Configure logging
logger = logging.getLogger(__name__)


def checker_agent(state: AgentState) -> AgentState:
    """
    Checker agent that evaluates SQL query results and sets traffic light status.
    """
    logger.info(f"Running Checker agent")
    state.active_agent = "checker"

    # Format query results for display
    results_display = "No results returned"
    if state.query_results:
        results_display = str(state.query_results[:5])
    elif state.query_error:
        results_display = f"Error: {state.query_error}"

    # Create the checker prompt
    checker_prompt = ChatPromptTemplate.from_template(
        """
        You are the Quality Checker agent, responsible for evaluating SQL query results
        to ensure they correctly answer the user's question.

        {checker_instruction}

        Database Schema:
        {database_schema}

        User Question:
        {user_question}

        Orchestrator Instructions:
        {orchestrator_instructions}

        SQL Query:
        {sql_query}

        Query Results:
        {results_display}

        Evaluate if these results satisfy the user's question. Set a traffic light status:
        - GREEN: Results fully satisfy the user's question
        - RED: Results need improvement (specify what's wrong)

        Return your response in the following format:
        TRAFFIC_LIGHT: [GREEN or RED]
        FEEDBACK: [Your detailed feedback explaining why]
        """
    )

    # Run the model
    model = get_model("gemini-2.0-flash-001")
    chain = checker_prompt | model | StrOutputParser()

    # Skip evaluation if there was a query error
    if state.query_error:
        state.traffic_light = "red"
        state.checker_feedback = f"SQL query failed with error: {state.query_error}"
        return state

    # Execute the chain
    response = chain.invoke({
        "checker_instruction": CHECKER_INSTRUCTION,
        "database_schema": DATABASE_SCHEMA,
        "user_question": state.user_question,
        "orchestrator_instructions": state.orchestrator_instructions,
        "sql_query": state.sql_query,
        "results_display": results_display
    })

    # Extract traffic light and feedback
    traffic_light_match = re.search(r"TRAFFIC_LIGHT:\s*(GREEN|RED)", response, re.IGNORECASE)
    feedback_match = re.search(r"FEEDBACK:\s*(.*?)(?:\n|$)", response, re.DOTALL | re.IGNORECASE)

    traffic_light = "yellow"  # Default
    if traffic_light_match:
        traffic_light = traffic_light_match.group(1).lower()
        if traffic_light == "green":
            traffic_light = "green"
        else:
            traffic_light = "red"

    feedback = ""
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    # Update state
    state.traffic_light = traffic_light
    state.checker_feedback = feedback
    logger.info(f"Checker evaluation complete. Traffic light: {traffic_light}")

    return state
