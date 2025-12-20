# 1. Use the official lightweight Python image
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory
WORKDIR /app

# 4. Install dependencies
# Note: Ensure 'requests' is in your requirements.txt for the Jira client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all application code
# This includes api.py, worker.py, review_classifier.html, and the modules/ folder
COPY . .

# 6. Expose the API port
EXPOSE 8002

# 7. Start BOTH services in a single line
# We launch worker.py in the background (&) and uvicorn in the foreground.
# If the container stops, both processes are terminated and restarted together.
CMD ["sh", "-c", "python worker.py & uvicorn api:app --host 0.0.0.0 --port 8002"]