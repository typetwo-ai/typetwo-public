from vertexai.preview.generative_models import GenerativeModel, Content, Part
from database_schema import DATABASE_SCHEMA, PROTEIN_MAPPING
from task_description import PROMPT_1_INSTRUCTION

query = '''
You have the SQL query and the search results.
If the results are correct, then just write the sql query again as a response.
If there is an error, understand the error, and correct the sql code. Make sure to use mysql.
In a response give just a clean and valid mysql code.


SELECT
    cp.ALOGP,
    a.PCHEMBL_VALUE,
    a.STANDARD_UNITS
FROM
    compound_properties cp
JOIN
    activities a ON cp.MOLREGNO = a.MOLREGNO
JOIN
    assays ass ON a.ASSAY_ID = ass.ASSAY_ID
JOIN
    target_dictionary td ON ass.TID = td.TID
WHERE
    td.chembl_id = 'CHEMBL204'
LIMIT 50;


[{'ALOGP': 1.11, 'PCHEMBL_VALUE': 10.0, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.15, 'PCHEMBL_VALUE': 10.05, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.06, 'PCHEMBL_VALUE': 9.89, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.49, 'PCHEMBL_VALUE': 9.48, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 2.69, 'PCHEMBL_VALUE': 9.14, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 1.54, 'PCHEMBL_VALUE': 7.1, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 1.53, 'PCHEMBL_VALUE': 8.49, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.04, 'PCHEMBL_VALUE': 8.67, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.85, 'PCHEMBL_VALUE': 5.58, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 1.04, 'PCHEMBL_VALUE': 9.59, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.4, 'PCHEMBL_VALUE': 8.3, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.61, 'PCHEMBL_VALUE': 7.72, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 0.29, 'PCHEMBL_VALUE': 7.37, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.22, 'PCHEMBL_VALUE': 7.8, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 0.29, 'PCHEMBL_VALUE': 6.58, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 0.42, 'PCHEMBL_VALUE': 7.14, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 0.42, 'PCHEMBL_VALUE': 6.51, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.97, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.43, 'PCHEMBL_VALUE': 8.08, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.4, 'PCHEMBL_VALUE': 7.72, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.31, 'PCHEMBL_VALUE': 7.26, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.72, 'PCHEMBL_VALUE': 9.15, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.66, 'PCHEMBL_VALUE': 8.68, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.11, 'PCHEMBL_VALUE': 8.21, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.5, 'PCHEMBL_VALUE': 6.9, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.27, 'PCHEMBL_VALUE': 7.83, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 0.13, 'PCHEMBL_VALUE': 6.33, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.05, 'PCHEMBL_VALUE': 5.86, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.27, 'PCHEMBL_VALUE': 6.71, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -1.07, 'PCHEMBL_VALUE': 7.5, 'STANDARD_UNITS': 'nM'}, {'ALOGP': -0.66, 'PCHEMBL_VALUE': 6.86, 'STANDARD_UNITS': 'nM'}, {'ALOGP': 4.86, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 4.22, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.63, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 3.91, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 4.23, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.49, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 6.05, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.99, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 3.91, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.38, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 4.99, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 3.6, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 4.21, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.5, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.2, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 5.38, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 4.87, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 6.13, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}, {'ALOGP': 3.45, 'PCHEMBL_VALUE': None, 'STANDARD_UNITS': 'l M-1'}]
'''

def main():
    model = GenerativeModel(model_name="gemini-2.0-flash-exp")

    response = model.generate_content(
        contents=[
            Content(role="user", parts=[Part.from_text(query)])
        ]
    )

    print(response)
    text = response.candidates[0].content.parts[0].text
    print(text)

if __name__ == "__main__":
    main()

