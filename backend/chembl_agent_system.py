import logging
import traceback
from typing import Dict, Any, TypeVar

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from agent_state import AgentState

from backend.agents.orchestrator_agent import orchestrator_agent
from backend.agents.writer_agent import writer_agent
from backend.agents.checker_agent import checker_agent
from backend.agents.reporter_agent import reporter_agent

# Configure logging
logger = logging.getLogger(__name__)

# Define state type for the graph
State = TypeVar("State", bound=AgentState)


class DatabaseAgentSystem:
    """
    Database agent system implemented using LangGraph for dynamic agent workflows
    with state management and conditional branching based on a traffic light system.
    """

    def __init__(self):
        """Initialize the database agent system."""
        self.graph = self._build_agent_graph()

    def _build_agent_graph(self) -> CompiledStateGraph:
        """
        Build the agent workflow graph using LangGraph.
        Defines the agents, their connections, and conditional logic.
        """
        # Create the graph with our state
        graph = StateGraph(AgentState)

        # Add all nodes (agents)
        graph.add_node("orchestrator", orchestrator_agent)
        graph.add_node("writer", writer_agent)
        graph.add_node("checker", checker_agent)
        graph.add_node("reporter", reporter_agent)

        # Define the edges - the flow of the workflow
        # Start with orchestrator
        graph.add_edge("orchestrator", "writer")

        # Writer always goes to checker
        graph.add_edge("writer", "checker")

        # Checker conditionally goes to either reporter (green) or writer (red)
        # This is where the traffic light logic is implemented

        # First, define the conditional routing
        def route_checker_output(state: AgentState) -> str:
            """
            Route based on the traffic light status.
            - GREEN: Go to reporter
            - RED: Go back to writer if under max iterations, otherwise end
            """
            if state.traffic_light == "green":
                logger.info("Traffic light is GREEN, proceeding to reporter")
                return "reporter"
            elif state.should_continue():
                logger.info(
                    f"Traffic light is RED, iteration {state.iteration_count}/{state.max_iterations}, going back to writer")
                return "writer"
            else:
                logger.info(
                    f"Traffic light is RED but reached max iterations ({state.max_iterations}), ending workflow")
                return END

        graph.add_conditional_edges(
            "checker",
            route_checker_output,
            {
                "reporter": "reporter",
                "writer": "writer",
                END: END
            }
        )

        # Reporter is the final step, ends after completion
        graph.add_edge("reporter", END)

        # Define the entry point
        graph.set_entry_point("orchestrator")

        # Compile the graph
        return graph.compile()

    def run_agent_graph(self, user_question: str) -> Dict[str, Any]:
        """
        Run the agent graph for a user question.

        Args:
            user_question: The question provided by the user

        Returns:
            The final state of the graph execution with all results
        """
        try:
            # Initialize the state with the user question
            initial_state = AgentState(user_question=user_question)

            # Configuration for the graph run
            config = RunnableConfig(
                recursion_limit=5,  # Prevent infinite loops
                callbacks=None  # Add callbacks here if needed
            )

            # Execute the graph
            logger.info(f"Starting agent graph execution for: {user_question}")
            result = self.graph.invoke(initial_state, config)
            logger.info("Agent graph execution completed successfully")

            return result

        except Exception as e:
            logger.error(f"Error in agent graph execution: {str(e)}")
            logger.error(traceback.format_exc())

            # Create a minimal result with error information
            error_state = AgentState(
                user_question=user_question,
                reporter_summary=f"Sorry, I encountered an error while processing your question: {str(e)}"
            )

            return {"state": error_state}