import functions_framework
from google.cloud import scheduler_v1
from google.protobuf import duration_pb2
import json
from google.auth import default

@functions_framework.http
def schedule_validation(request):
    credentials, _ = default(scopes=['https://www.googleapis.com/auth/cloud-scheduler'])
    client = scheduler_v1.CloudSchedulerClient(credentials=credentials)

    request_json = request.get_json()
    cron = request_json['cron']
    gs_name = request_json['gs_name']
    name = request_json['name']
    
    PROJECT_ID = "tfg-dq"
    LOCATION_ID = "europe-west3"
    JOB_ID = f"dq_scheduler_{gs_name}"
    
    URI = f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation"
    MESSAGE_BODY = {
        "name": name,
        "gs_name": gs_name
    }
    TIME_ZONE = "Etc/UTC"
    message_body_json = json.dumps(MESSAGE_BODY).encode()

    parent = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    job_name = f"{parent}/jobs/{JOB_ID}"

    http_target = scheduler_v1.HttpTarget(
        uri=URI,
        http_method=scheduler_v1.HttpMethod.POST,
        headers={"Content-Type": "application/json"},
        body=message_body_json
    )

    job = {
        "name": job_name,
        "http_target": http_target,
        "schedule": cron,
        "time_zone": TIME_ZONE,
        "retry_config": {
            "retry_count": 3,
            "max_retry_duration": duration_pb2.Duration(seconds=3600),
            "min_backoff_duration": duration_pb2.Duration(seconds=5),
            "max_backoff_duration": duration_pb2.Duration(seconds=3600),
            "max_doublings": 3
        },
        "attempt_deadline": duration_pb2.Duration(seconds=180)
    }

    try:
        get_job = scheduler_v1.GetJobRequest(name=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}")
        response = client.get_job(request=get_job)
        print(response)
        print(f"Ya existe una programación para esta matriz: {gs_name}\nSe actualizarán los valores.")
        
        update_job = scheduler_v1.UpdateJobRequest(job=job)
        response = client.update_job(request=update_job)
        print("Updated job:", response.name)
    except:
        print(f"No existe ninguna programación para esta matriz: {gs_name}\nSe creará una nueva.")

        request = scheduler_v1.CreateJobRequest(job=job, parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}")
        response = client.create_job(request={"parent": parent, "job": job})
        print("Created job:", response.name)
    
    return "Scheduler configurado"