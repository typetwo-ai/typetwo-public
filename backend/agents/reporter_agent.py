import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.agent_state import AgentState
from backend.task_description import (
    REPORTER_INSTRUCTION
)

from backend.agents.utils import get_model

logger = logging.getLogger(__name__)


def reporter_agent(state: AgentState) -> AgentState:
    """
    Reporter agent that generates clear summaries of the query results.
    """
    logger.info(f"Running Reporter agent")
    state.active_agent = "reporter"

    # Format query results for display
    results_display = "No results returned"
    if state.query_results:
        results_display = str(state.query_results)

    # Create the reporter prompt
    reporter_prompt = ChatPromptTemplate.from_template(
        """
        You are the Data Reporter agent, responsible for creating clear, concise
        summaries of database query results that directly answer the user's question.

        {reporter_instruction}

        User Question:
        {user_question}

        Orchestrator Instructions:
        {orchestrator_instructions}

        SQL Query:
        {sql_query}

        Query Results:
        {results_display}

        Create a clear summary that directly answers the user's question.
        Focus on insights, patterns, and key data points.
        """
    )

    # Run the model
    model = get_model("gemini-2.0-pro-exp-02-05")
    chain = reporter_prompt | model | StrOutputParser()

    # Execute the chain
    summary = chain.invoke({
        "reporter_instruction": REPORTER_INSTRUCTION,
        "user_question": state.user_question,
        "orchestrator_instructions": state.orchestrator_instructions,
        "sql_query": state.sql_query,
        "results_display": results_display
    })

    # Update state
    state.reporter_summary = summary
    logger.info(f"Reporter summary generated successfully")

    return state
