import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL") or "http://localhost:8000"
stats = requests.get(f"{BACKEND_URL}/statistics").json()

st.title("Analytics Dashboard")

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

