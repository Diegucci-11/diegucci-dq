import functions_framework
import google.auth
import google.auth.transport.requests
from google.cloud import storage

project_id = 'tfg-dq'
location = 'europe-southwest1'
composer_environment = 'composer-test-1'

@functions_framework.http
def create_dag_dq(request):
    data = request.get_json()

    with open('dq_dag.txt', 'r') as file:
        contenido = file.read()

    DAG_NAME_SENTENCE = f'DAG_NAME = "dag_dq_{data["dag_name"]}"'
    DAG_CRON_SENTENCE = f'CRON = "{data["dag_cron"]}"'
    DAG_YML_SENTENCE = f'YML = "dq_yaml_{data["dag_name"]}"'

    contenido_modificado = contenido.replace('DAG_NAME = "dq_validation_dag"', DAG_NAME_SENTENCE)
    contenido_modificado = contenido_modificado.replace('CRON = "0 0 1 * *""', DAG_CRON_SENTENCE)
    contenido_modificado = contenido_modificado.replace('YML = "yml.yml""', DAG_YML_SENTENCE)

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    authed_session = google.auth.transport.requests.AuthorizedSession(credentials)

    url = f"https://composer.googleapis.com/v1beta1/projects/{project_id}/locations/{location}/environments/{composer_environment}"
    response = authed_session.request("GET", url)

    environment_data = response.json()
    ruta_bucket = environment_data["config"]["dagGcsPrefix"]

    storage_client = storage.Client()

    ruta_split = ruta_bucket.split("/")
    nombre_bucket = ruta_split[2]
    ruta_dentro_bucket = "/".join(ruta_split[3:])

    bucket = storage_client.bucket(nombre_bucket)
    blob = bucket.blob(ruta_dentro_bucket + "/" + "dq_dag.py")

    blob.upload_from_string(contenido_modificado)

    return "dag creado correctamente", 200
