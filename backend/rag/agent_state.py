from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    original_question: str
    rephrased_question: str
    retrieved_context: List[Dict[str, Any]]
    filtered_context: List[Dict[str, Any]]
    answer: str
