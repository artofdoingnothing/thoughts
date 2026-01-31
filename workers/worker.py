import os
import sys
from redis import Redis
from rq import Worker, Queue
from libs.db_service import init_database

# Connect to Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

# Get queues from environment variable, default to 'default'
listen = os.getenv("QUEUES", "default").split(",")

def run_worker():
    # Initialize DB connection for the worker process
    init_database()
    
    print(f"Worker listening on queues: {listen}")
    
    # Pass connection directly to Worker and Queue
    queues = [Queue(name, connection=redis_conn) for name in listen]
    worker = Worker(queues, connection=redis_conn)
    worker.work()

if __name__ == '__main__':
    run_worker()
