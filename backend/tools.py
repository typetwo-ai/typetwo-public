import logging
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool

# Import your existing utility functions
from utils import execute_query

# Configure logging
logger = logging.getLogger(__name__)


class SQLExecutionTool(BaseTool):
    """Tool for executing SQL queries against the database"""

    def __init__(self):
        super().__init__(
            name="SQL Execution Tool",
            description="""
            Execute a SQL query on the database and return the results.
            This tool requires a valid SQL query as input and will return either
            the query results or an error message.
            """
        )

    def _run(self, query: str) -> Dict[str, Any]:
        """
        Execute the SQL query and return the results or an error

        Args:
            query: The SQL query to execute

        Returns:
            A dictionary with the query results or an error message
        """
        logger.info(f"Executing SQL query: {query[:100]}...")
        try:
            # Use your existing execute_query function
            results = execute_query(query)
            logger.info(
                f"Query executed successfully. Got {len(results) if isinstance(results, list) else 'error'} results")
            return {
                "sql_query": query,
                "query_results": results,
                "error": None
            }
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return {
                "sql_query": query,
                "query_results": [],
                "error": str(e)
            }


class QueryEvaluationTool(BaseTool):
    """Tool for evaluating query results against user requirements"""

    def __init__(self):
        super().__init__(
            name="Query Evaluation Tool",
            description="""
            Evaluate SQL query results to determine if they satisfy the user's requirements.
            This tool helps determine if the traffic light should be green (satisfactory)
            or red (needs improvement).
            """
        )

    def _run(
            self,
            query_results: List[Dict[str, Any]],
            user_question: str,
            expected_attributes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate the query results to determine if they satisfy requirements

        Args:
            query_results: Results from the SQL query
            user_question: The original user question
            expected_attributes: Optional list of expected attributes

        Returns:
            A dictionary with the evaluation result
        """
        # Basic validation checks
        if not query_results or (isinstance(query_results, list) and len(query_results) == 0):
            return {
                "traffic_light": "red",
                "evaluation_reason": "Query returned no results"
            }

        if isinstance(query_results, str) and "error" in query_results.lower():
            return {
                "traffic_light": "red",
                "evaluation_reason": f"Query execution failed: {query_results}"
            }

        # If expected attributes are provided, check they exist in results
        if expected_attributes and isinstance(query_results, list) and len(query_results) > 0:
            first_result = query_results[0]
            missing_attributes = [attr for attr in expected_attributes if attr not in first_result]
            if missing_attributes:
                return {
                    "traffic_light": "red",
                    "evaluation_reason": f"Missing expected attributes: {', '.join(missing_attributes)}"
                }

        # Basic checks pass, default to green
        return {
            "traffic_light": "green",
            "evaluation_reason": "Query results appear to satisfy the requirements"
        }
