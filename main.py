from fastapi import FastAPI, UploadFile, File
from redis import Redis
from rq import Queue
from rq.job import Job

from tasks import classify_task


app = FastAPI()

redis_conn = Redis()
queue = Queue(connection=redis_conn)


@app.get("/") #when sends GET, run fuction
def root():
    return {"Status": "API is running"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    image_bytes = await file.read()
    job = queue.enqueue(classify_task, image_bytes)
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)
    if job.is_finished:
        return {"status": "finished", "result": job.result}
    elif job.is_failed:
        return {"status": "failed"}
    else:
        return {"status": job.get_status()}

