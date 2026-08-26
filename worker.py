import os
from redis import Redis
from rq import Queue, Worker

redis_conn = Redis(host=os.environ.get("REDIS_HOST", "localhost"))
queue = Queue(connection=redis_conn)

if __name__ == "__main__":
    worker = Worker([queue], connection=redis_conn)
    worker.work()