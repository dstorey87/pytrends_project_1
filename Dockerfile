FROM python:3.10-slim

WORKDIR /app

COPY requirements_worker.txt .
RUN pip install --no-cache-dir -r requirements_worker.txt

COPY worker_tasks.py .
COPY celery_config.py .

# Create a non-root user and switch to it
RUN useradd -ms /bin/bash celery_user
USER celery_user

CMD ["celery", "-A", "worker_tasks", "worker", "--loglevel=info"]
