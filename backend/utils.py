from decimal import Decimal
from google.cloud import bigquery
import mysql.connector

# def execute_query(query: str) -> str | list[dict]:
#     try:
#         client = bigquery.Client()
#         results = client.query(query).to_dataframe()
#         results = results.to_dict('records')
#         for row in results:
#             for key, value in row.items():
#                 if isinstance(value, Decimal):
#                     row[key] = float(value)
#         return results 
#     except Exception as e:
#         return f"Error: {e}"
    
def execute_query(query: str) -> str | list[dict]:
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