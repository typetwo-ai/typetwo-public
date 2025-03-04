import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.agent_state import AgentState
from backend.task_description import (
    ORCHESTRATOR_INSTRUCTION
)

from backend.agents.utils import get_model

from backend.database_schema import DATABASE_SCHEMA

logger = logging.getLogger(__name__)


def orchestrator_agent(state: AgentState) -> AgentState:
    """
    Orchestrator agent that interprets user questions and provides
    instructions for the SQL Writer.
    """
    logger.info(f"Running Orchestrator agent for query: {state.user_question}")
    state.active_agent = "orchestrator"

    # Create the orchestrator prompt
    orchestrator_prompt = ChatPromptTemplate.from_template(ORCHESTRATOR_INSTRUCTION)

    # Run the model
    model = get_model("gemini-2.0-pro-exp-02-05")
    chain = orchestrator_prompt | model | StrOutputParser()

    # Execute the chain
    instructions = chain.invoke({
        "user_question": state.user_question,
        "orchestrator_instruction": ORCHESTRATOR_INSTRUCTION,
        "database_schema": DATABASE_SCHEMA
    })

    # Update state
    state.orchestrator_instructions = instructions
    logger.info(f"Orchestrator instructions generated successfully")

    return state
