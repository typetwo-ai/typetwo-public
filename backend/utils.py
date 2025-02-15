from decimal import Decimal
from google.cloud import bigquery

def execute_query(query: str) -> str | list[dict]:
    try:
        client = bigquery.Client()
        results = client.query(query).to_dataframe()
        results = results.to_dict('records')
        for row in results:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        return results 
    except Exception as e:
        return f"Error: {e}"