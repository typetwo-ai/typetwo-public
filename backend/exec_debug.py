import plotly.express as px

third_response: str = '''
import plotly.express as px

data = [
    {'MOLREGNO': 115, 'CX_LOGP': 1.16, 'MW_FREEBASE': 162.24},
    {'MOLREGNO': 116, 'CX_LOGP': 0.78, 'MW_FREEBASE': 148.21},
    {'MOLREGNO': 188, 'CX_LOGP': -1.48, 'MW_FREEBASE': 119.12},
    {'MOLREGNO': 238, 'CX_LOGP': 2.67, 'MW_FREEBASE': 180.23},
    {'MOLREGNO': 242, 'CX_LOGP': 1.97, 'MW_FREEBASE': 159.23}
]

figure = px.scatter(
    data_frame=data,
    x='CX_LOGP',
    y='MW_FREEBASE',
    text='MOLREGNO',
    title='Scatter Plot of LogP vs MW for Compounds',
    labels={'CX_LOGP': 'LogP', 'MW_FREEBASE': 'Molecular Weight (MW)'},
    template='plotly'
)

figure.update_traces(textposition='top center')
'''

def generate_figure(response: str):
   try:
       local_namespace = {}
       exec(response, globals(), local_namespace)
       figure = local_namespace['figure']
       print(f"exec() ran successfully: {figure}") if figure else print("exec() ran successfully, but no figure found")
       return figure
   except Exception as e:
       print(f"Error running exec(): {e}")
       return None

if __name__ == "__main__":
   generate_figure(third_response)