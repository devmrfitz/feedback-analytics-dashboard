import json
import os
import time

import redis
from tasktiger import TaskTiger

from feedbackprocessing import process_feedback_impl

REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or 6379

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
tiger = TaskTiger(r)


@tiger.task(retry=True)
def process_feedback(payload: dict):
    task_id = tiger.current_task.id
    payload["status"] = "EXECUTING"
    r.hset("feedback", task_id, json.dumps(payload, default=str))
    result = process_feedback_impl(payload)

    payload["status"] = "COMPLETED"
    payload["request_completed_at"] = str(time.time())

    result_payload = {**payload, **result, "task_id": task_id}
    print("Result payload: ", result_payload)
    result_payload = json.dumps(result_payload, default=str)
    r.hset("feedback", task_id, result_payload)
