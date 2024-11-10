# Use Python slim image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements_worker.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_worker.txt

# Now copy the rest of the application files
COPY . /app

# Define the command to run the worker
CMD ["celery", "-A", "worker_tasks", "worker", "--loglevel=info"]
