# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install dependencies only once
COPY requirements_worker.txt /app/
RUN pip install --no-cache-dir -r requirements_worker.txt

# Mount persistent storage for caches
VOLUME /root/.cache/huggingface  # For Hugging Face transformers
VOLUME /root/.cache/pip          # For pip cache

# Copy the worker-related files
COPY worker_tasks.py /app/
COPY celery_config.py /app/

# Default command for the worker
CMD ["celery", "-A", "worker_tasks", "worker", "--loglevel=info"]
