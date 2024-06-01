import functions_framework
from google.cloud import scheduler_v1
from google.protobuf import duration_pb2
from google.protobuf import json_format
import json
from google.auth import default
import subprocess

@functions_framework.http
def schedule_validation(request):
    credentials, _ = default(scopes=['https://www.googleapis.com/auth/cloud-scheduler'])

    request_json = request.get_json()
    cron = request_json['cron']
    gs_name = request_json['gs_name']
    name = request_json['name']
    
    PROJECT_ID = "tfg-dq"
    LOCATION_ID = "europe-west3"
    JOB_ID = f"dq_scheduler_{gs_name}"
    
    # client = scheduler_v1.CloudSchedulerClient(credentials=credentials)

    # body_dict = {"name": name, "gs_name": gs_name}
    # body_bytes = json.dumps(body_dict).encode('utf-8')

    # attempt_deadline = duration_pb2.Duration()
    # attempt_deadline.seconds = 180

    # retry_config = scheduler_v1.types.RetryConfig()
    # retry_config.retry_count = 3
    # retry_config.max_retry_duration = duration_pb2.Duration(seconds=600)
    # retry_config.min_backoff_duration = duration_pb2.Duration(seconds=5)
    # retry_config.max_backoff_duration = duration_pb2.Duration(seconds=3600)
    # retry_config.max_doublings = 5

    # req = scheduler_v1.types.HttpMethod()
    # req.uri = f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation"
    # req.http_method = "POST"
    # req.body = b'{"name": "name", "gs_name": "gs_name"}'
    # req.headers = {"Content-type": "application/json"}

    # job = scheduler_v1.types.Job()
    # job.name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}"
    # job.http_target = req
    # job.schedule = cron
    # job.time_zone = "Etc/UTC"
    # job.retry_config=retry_config,
    # job.attempt_deadline=attempt_deadline

    # job = {
    #     "name": f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}",
    #     "http_target": {
    #         "uri": f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation",
    #         "http_method": "POST",
    #         "body": b'{"name": "name", "gs_name": "gs_name"}',
    #         "headers": {"Content-type": "application/json"}
    #     },
    #     "schedule": cron,
    #     "time_zone": "Etc/UTC",
    #     "retry_config": {
    #         "retry_count": 3,
    #         "max_retry_duration": {
    #             "seconds": 3600 
    #         },
    #         "min_backoff_duration": {
    #             "seconds": 5
    #         },
    #         "max_backoff_duration": {
    #             "seconds": 3600
    #         },
    #         "max_doublings": 3
    #     },
    #     "attempt_deadline": {
    #         "seconds": 180
    #     }
    # }

    # job = json_format.ParseDict(job, scheduler_v1.types.Job())

    URI = f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation"
    MESSAGE_BODY = {
        "name": name,
        "gs_name": gs_name
    }
    TIME_ZONE = "Etc/UTC"
    message_body_json = json.dumps(MESSAGE_BODY)

    gcloud_command = f"gcloud scheduler jobs create http {JOB_ID} --schedule={cron} --location={LOCATION_ID} --uri={URI} --message-body={message_body_json} --time-zone={TIME_ZONE} --http-method=POST"

    try:
        result = subprocess.run(gcloud_command, shell=True, capture_output=True, text=True)
        print("Job creado exitosamente:")
        print(result.stdout)
        print("Errores si hay:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error al crear el job:", e.stderr)

    if result.stderr:
        print("Error en el comando gcloud:")
        print(result.stderr)


    # try:
    #     get_job = scheduler_v1.GetJobRequest(name=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}")
    #     response = client.get_job(request=get_job)
    #     print(response)
    #     print(f"Ya existe una programación para esta matriz: {gs_name}\nSe actualizarán los valores.")
        
    #     update_job = scheduler_v1.UpdateJobRequest(job=job)
    #     response = client.update_job(request=update_job)
    #     print(response)
    # except:
    #     print(f"No existe ninguna programación para esta matriz: {gs_name}\nSe creará una nueva.")

    #     request = scheduler_v1.CreateJobRequest(job=job, parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}")
    #     response = client.create_job(request=request)
    #     print(response)
    
    return "Scheduler configurado"