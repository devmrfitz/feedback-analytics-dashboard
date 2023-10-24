import json
import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL") or "http://localhost:8000"

stats = requests.get(f"{BACKEND_URL}/statistics").json()

st.title("Feedback analysis")

st.subheader("Sample analysis request")

feedback = st.text_input("Enter feedback")
platform = st.selectbox("Select platform", ["LinkedIn", "Twitter", "Email"])


def send_analysis_request():
    payload = {
        "feedback": feedback,
        "metadata": {
            "source_platform": platform
        }
    }
    response = requests.post(f"{BACKEND_URL}/tasks", data=json.dumps(payload),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        st.info(f"Task created successfully. Task ID: {response.json().get('task_id')}")
    else:
        st.error(f"Error creating task. Error: {response.json()}")


st.button("Send request", on_click=send_analysis_request)

st.subheader("Status")

task_id = st.text_input("Enter task ID")


def get_task_status():
    response = requests.get(f"{BACKEND_URL}/tasks/{task_id}")
    if response.status_code == 200:
        st.info(f"Task status: {response.json().get('status')}")
    else:
        st.error(f"Error getting task status. Error: {response.json()}")


st.button("Get status", on_click=get_task_status)


st.subheader("Statistics")
# Show total number of tasks processed
st.text(f"Total number of tasks processed: {stats.get('tasks_processed')}")
st.text(f"Average processing time per task: {stats.get('average_processing_time')} seconds")

# Show total number of tasks processed per platform using a bar chart
st.subheader("Total number of tasks processed per platform")
st.bar_chart(stats.get("tasks_processed_per_platform"))

# Show sentiment distribution using a pie chart using matplotlib
st.subheader("Sentiment distribution")
st.bar_chart(stats.get("sentiment_distribution"))

# Show topic distribution using a pie chart using matplotlib
st.subheader("Topic distribution")
st.bar_chart(stats.get("topic_distribution"))
