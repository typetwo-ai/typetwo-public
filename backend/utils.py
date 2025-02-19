from decimal import Decimal
import mysql.connector
    
def execute_query(query: str) -> list[dict] | str:
    """Executes an SQL query on the ChEMBL database and returns the results.

    Args:
        query (str): The SQL query to execute.

    Returns:
        A list of dictionaries representing the query results, where each dictionary represents a row and
            maps column names to values. Decimal values are converted to floats.
        A string containing an error message if an exception occurs.
    """
    try:
        conn = mysql.connector.connect(
            unix_socket='/cloudsql/project-1-450712:us-central1:chembl35-instance', # host='35.184.138.61' for local, unix_socket='/cloudsql/project-1-450712:us-central1:chembl35-instance' for cloud
            user='root',
            password='chembl',
            database='chembl_35'
        )
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