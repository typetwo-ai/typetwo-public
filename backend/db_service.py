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

if __name__ == "__main__":
    test_query: str = "SELECT t1.CHEMBL_ID, t2.PREF_NAME FROM `patents-public-data.ebi_chembl.chembl_id_lookup` AS t1 INNER JOIN `patents-public-data.ebi_chembl.molecule_dictionary` AS t2 ON t1.ENTITY_ID = t2.MOLREGNO WHERE t1.CHEMBL_ID = "
    print("Executing test query...")
    test_results: str | list[tuple] = execute_query(test_query)
    if isinstance(test_results, list):
        for row in test_results:
            print(row)
    else:
        print(test_results)
