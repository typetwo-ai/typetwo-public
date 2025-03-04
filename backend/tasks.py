from typing import Dict, List, Any, Optional
from crewai import Task


def create_orchestrator_task(user_question: str) -> Task:
    """
    Create a task for the Orchestrator agent to interpret the user's question
    and provide guidance for the Writer agent.

    Args:
        user_question: The original question from the user

    Returns:
        A CrewAI Task for the Orchestrator agent
    """
    return Task(
        description=f"""
        Analyze this user question and provide detailed instructions for creating an SQL query:

        USER QUESTION:
        {user_question}

        Your job is to:
        1. Understand what information the user is looking for
        2. Identify which database tables and columns are needed
        3. Determine any filtering, sorting, or aggregation needed
        4. Provide clear instructions for the Writer agent

        Focus on providing complete and detailed instructions that will lead to a query that fully
        answers the user's original question.
        """,
        expected_output="""
        Provide a detailed analysis of the user's question and clear instructions for creating
        an SQL query. Your output should be structured as follows:

        {
            "orchestrator_output": "Your detailed instructions here"
        }
        """,
        agent_role="Orchestrator"
    )


def create_writer_task(
        user_question: str,
        orchestrator_input: str,
        previous_query: str,
        previous_result: Any
) -> Task:
    """
    Create a task for the Writer agent to generate an SQL query
    based on the Orchestrator's instructions.

    Args:
        user_question: The original question from the user
        orchestrator_input: Instructions from the Orchestrator agent
        previous_query: Previous SQL query (if any)
        previous_result: Results from the previous query (if any)

    Returns:
        A CrewAI Task for the Writer agent
    """
    # Format the previous results for display
    if isinstance(previous_result, list) and previous_result:
        previous_result_display = str(previous_result[:5])
    else:
        previous_result_display = str(previous_result)

    return Task(
        description=f"""
        Generate a SQL query to answer this user question:

        USER QUESTION:
        {user_question}

        ORCHESTRATOR INSTRUCTIONS:
        {orchestrator_input}

        PREVIOUS SQL QUERY (if any):
        {previous_query}

        PREVIOUS QUERY RESULTS (if any):
        {previous_result_display}

        Your task is to:
        1. Create a precise SQL query that answers the user question
        2. Make sure the query follows correct MySQL syntax
        3. Use appropriate joins, filters, and aggregations
        4. Address any issues found in previous query attempts

        Use the sql_execution_tool to run your query and see the results.
        """,
        expected_output="""
        Provide your final SQL query and the results of executing it. Format your output as:

        {
            "sql_query": "Your SQL query here",
            "query_results": [The results from executing the query]
        }
        """,
        agent_role="SQL Writer",
        tools=["sql_execution_tool"]
    )


def create_checker_task(
        user_question: str,
        orchestrator_input: str,
        sql_query: str,
        query_results: Any
) -> Task:
    """
    Create a task for the Checker agent to evaluate the SQL query results
    and determine if they satisfy the user's question.

    Args:
        user_question: The original question from the user
        orchestrator_input: Instructions from the Orchestrator agent
        sql_query: The SQL query to evaluate
        query_results: The results from executing the SQL query

    Returns:
        A CrewAI Task for the Checker agent
    """
    # Format the query results for display
    if isinstance(query_results, list) and query_results:
        query_results_display = str(query_results[:5])
    else:
        query_results_display = str(query_results)

    return Task(
        description=f"""
        Evaluate if these SQL query results satisfy the user's question:

        USER QUESTION:
        {user_question}

        ORCHESTRATOR INSTRUCTIONS:
        {orchestrator_input}

        SQL QUERY:
        {sql_query}

        QUERY RESULTS:
        {query_results_display}

        Your task is to:
        1. Check if the query correctly addresses all aspects of the user's question
        2. Verify the results contain the information requested
        3. Determine if the data format is appropriate
        4. Set a traffic light status (green or red)

        Use the query_evaluation_tool to help with your analysis.
        """,
        expected_output="""
        Provide your evaluation and set the traffic light status. Format your output as:

        {
            "traffic_light": "green" or "red",
            "evaluation_reason": "Detailed explanation of your evaluation"
        }
        """,
        agent_role="Quality Checker",
        tools=["query_evaluation_tool"]
    )


def create_reporter_task(
        user_question: str,
        orchestrator_input: str,
        sql_query: str,
        query_results: Any
) -> Task:
    """
    Create a task for the Reporter agent to generate a clear summary
    of the query results for the end user.

    Args:
        user_question: The original question from the user
        orchestrator_input: Instructions from the Orchestrator agent
        sql_query: The SQL query used
        query_results: The results from executing the SQL query

    Returns:
        A CrewAI Task for the Reporter agent
    """
    # Format the query results for display
    if isinstance(query_results, list) and query_results:
        query_results_display = str(query_results)
    else:
        query_results_display = str(query_results)

    return Task(
        description=f"""
        Create a clear summary of these database query results that directly answers the user's question:

        USER QUESTION:
        {user_question}

        ORCHESTRATOR ANALYSIS:
        {orchestrator_input}

        SQL QUERY USED:
        {sql_query}

        QUERY RESULTS:
        {query_results_display}

        Your task is to:
        1. Summarize the key information from the query results
        2. Present the information in a clear, user-friendly way
        3. Directly address the user's original question
        4. Highlight any important patterns or insights in the data
        """,
        expected_output="""
        Provide a clear summary of the query results that directly answers the user's question.
        Format your output as:

        {
            "summary": "Your detailed but concise summary here"
        }
        """,
        agent_role="Data Reporter"
    )