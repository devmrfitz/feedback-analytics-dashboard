import json
import os
import time
from collections import defaultdict

import redis
import tasktiger
from fastapi import FastAPI
from pydantic import BaseModel
from tasktiger import Task

from worker import process_feedback


class PayloadMetadata(BaseModel):
    source_platform: str


class Payload(BaseModel):
    feedback: str
    metadata: PayloadMetadata


REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or 6379

app = FastAPI()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
tiger = tasktiger.TaskTiger(r)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tasks/")
async def create_task(payload: Payload):
    serialized_payload = payload.model_dump()
    serialized_payload["request_received_at"] = str(time.time())
    task = Task(tiger, process_feedback, args=[serialized_payload])
    task.delay()
    return {
        "task_id": task.id,
    }


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    if r.hget("feedback", task_id):
        return {
            "task_id": task_id,
            "status": json.loads(r.hget("feedback", task_id)).get("status"),
        }
    for task_state in ['queued', 'scheduled', 'active', 'error']:
        task = Task.from_id(tiger, 'default', task_state, task_id)
        if task:
            return {
                "task_id": task_id,
                "status": task_state.upper(),
            }
    return {
        "task_id": task_id,
    }


@app.get("/statistics")
async def get_statistics():
    tasks_processed = 1e-16  # Avoid division by zero
    tasks_processed_per_platform = defaultdict(int)
    total_processing_time = 0
    sentiment_distribution = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "NEUTRAL": 0,
    }
    topic_distribution = {
        "PRICING": 0,
        "PRODUCT_FEATURES": 0,
        "CUSTOMER_SERVICE": 0,
        "OTHER": 0,
    }

    for task_id in r.hkeys("feedback"):
        task = json.loads(r.hget("feedback", task_id))
        if task.get("status") == "COMPLETED":
            tasks_processed += 1
            total_processing_time += float(task.get("request_completed_at")) - float(task.get("request_received_at"))
            sentiment_distribution[task.get("sentiment")] += 1
            topic_distribution[task.get("topic")] += 1
            tasks_processed_per_platform[task.get("metadata").get("source_platform")] += 1

    return {
        "tasks_processed": int(tasks_processed),
        "average_processing_time": total_processing_time / tasks_processed,
        "sentiment_distribution": sentiment_distribution,
        "topic_distribution": topic_distribution,
        "tasks_processed_per_platform": tasks_processed_per_platform,
    }
