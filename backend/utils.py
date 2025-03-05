import re
from decimal import Decimal
import mysql.connector
import os


def execute_query(query: str, limit=100) -> list[dict] | str:
    """Executes an SQL query on the ChEMBL database and returns the results.

    Args:
        query (str): The SQL query to execute.

    Returns:
        A list of dictionaries representing the query results, where each dictionary represents a row and
            maps column names to values. Decimal values are converted to floats.
        A string containing an error message if an exception occurs.
    """
    try:
        if os.getenv("LOCAL_DEV"):  # Checks if running locally
            conn = mysql.connector.connect(
                host='35.184.138.61',
                user='root',
                password='chembl',
                database='chembl_35'
            )
        else:
            conn = mysql.connector.connect(
                unix_socket='/cloudsql/project-1-450712:us-central1:chembl35-instance',
                user='root',
                password='chembl',
                database='chembl_35'
            )

        query = remove_limit_clause(query)
        query += f" LIMIT {limit}"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"Error: {e}"


def remove_limit_clause(sql_query):
    pattern = r'\bLIMIT\s+\d+(?:\s*(?:,|\bOFFSET\b)\s*\d+)?\s*$'

    return re.sub(pattern, '', sql_query, flags=re.IGNORECASE).strip()
