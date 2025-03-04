from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Shared state for the database agent workflow.
    This is passed between agents in the LangGraph.
    """
    # Input and tracking
    user_question: str = ""
    iteration_count: int = 0
    max_iterations: int = 5

    # Orchestrator output
    orchestrator_instructions: str = ""

    # Writer output
    sql_queries: [str] = []
    query_results: List[Dict[str, Any]] = Field(default_factory=list)
    query_error: Optional[str] = None

    # Checker output
    traffic_light: str = "yellow"  # "green", "yellow", "red"
    checker_feedback: str = ""

    # Reporter output
    reporter_summary: str = ""

    # Tracking for visualization
    active_agent: Optional[str] = None

    def should_continue(self) -> bool:
        """
        Determine if the workflow should continue to the next iteration
        based on traffic light and iteration count.
        """
        # Continue if we have a red light and haven't reached max iterations
        return (
                self.traffic_light == "red" and
                self.iteration_count < self.max_iterations
        )
