from backend.rag.agent_state import AgentState


class BaseNode:
    def __call__(self, state: AgentState) -> AgentState:
        raise NotImplementedError("Subclasses must implement this method")