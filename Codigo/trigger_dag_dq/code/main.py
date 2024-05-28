import functions_framework
import requests
import composer2_airflow_rest_api

@functions_framework.http
def trigger_dag(request):
    data = request.get_json()
    
    dag_name = "dag_dq_" + data["dag_name"]
    url = "https://9e0265b75cfc4039b86bf61efc7fe69b-dot-europe-southwest1.composer.googleusercontent.com"

    return trigger_dag_gcf(dag_name, url)

def trigger_dag_gcf(dag_name, url, context=None):
    web_server_url = (url)

    try:
        composer2_airflow_rest_api.trigger_dag(web_server_url, dag_name, {})
        return "Ejecución activada", 200
    except requests.exceptions.HTTPError as err:
        return(f"Error HTTP: {err}"), 404
