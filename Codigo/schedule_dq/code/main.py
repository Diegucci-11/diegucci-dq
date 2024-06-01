import functions_framework
from google.cloud import scheduler_v1
from google.protobuf import json_format

@functions_framework.http
def schedule_validation(request):
    request_json = request.get_json()
    cron = request_json['cron']
    gs_name = request_json['gs_name']
    name = request_json['name']
    
    PROJECT_ID = "tfg-dq"
    LOCATION_ID = "europe-west3"
    JOB_ID = f"dq_scheduler_{gs_name}"
    
    client = scheduler_v1.CloudSchedulerClient()
    
    # req = scheduler_v1.types.HttpMethod()
    # req.uri = f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation"
    # req.http_method = "POST"
    # req.body = b'{"name": name, "gs_name": gs_name}'
    # req.headers = {"Content-type": "application/json"}

    # job = scheduler_v1.types.Job()
    # job.name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}"
    # job.http_target = req
    # job.schedule = cron
    # job.time_zone = "Etc/UTC"

    job = {
        "name": f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}",
        "http_target": {
            "uri": f"https://europe-southwest1-{PROJECT_ID}.cloudfunctions.net/dq_validation",
            "http_method": "POST",
            "body": {"name": name, "gs_name": gs_name},
            "headers": {"Content-type": "application/json"}
        },
        "schedule": cron,
        "time_zone": "Etc/UTC",
    }

    job = json_format.ParseDict(job, scheduler_v1.types.Job())

    try:
        get_job = scheduler_v1.GetJobRequest(name=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{JOB_ID}")
        response = client.get_job(request=get_job)
        print(response)
        print(f"Ya existe una programación para esta matriz: {gs_name}\nSe actualizarán los valores.")
        
        update_job = scheduler_v1.UpdateJobRequest(job=job)
        response = client.update_job(request=update_job)
        print(response)
    except:
        print(f"No existe ninguna programación para esta matriz: {gs_name}\nSe creará una nueva.")

        request = scheduler_v1.CreateJobRequest(job=job, parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}")
        response = client.create_job(request=request)
        print(response)
    
    return "Scheduler configurado"