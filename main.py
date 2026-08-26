import os
from fastapi import FastAPI, UploadFile, File
from redis import Redis
from rq import Queue
from rq.job import Job

from tasks import classify_task
from database import SessionLocal, JobRecord



app = FastAPI()

redis_conn = Redis(host=os.environ.get("REDIS_HOST", "localhost"))
queue = Queue(connection=redis_conn)


@app.get("/") #when sends GET, run fuction
def root():
    return {"Status": "API is running"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    image_bytes = await file.read()
    job = queue.enqueue(classify_task, image_bytes)
    db = SessionLocal()
    record = JobRecord(id=job.id, status="queued")
    db.add(record)
    db.commit()
    db.close()
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)
    db = SessionLocal()
    record = db.query(JobRecord).filter(JobRecord.id == job_id).first()

    if job.is_finished:
        record.status = "finished"
        record.result = job.result
        db.commit()
    elif job.is_failed:
        record.status = "failed"
        db.commit()

    status = record.status
    result = record.result
    db.close()

    return {"status": record.status, "result": record.result}

