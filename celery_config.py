from celery import Celery

# Celery configuration
app = Celery(
    "workers",
    broker="redis://redis:6379/0",  # Redis container in Docker Compose
    backend="redis://redis:6379/0"  # Result backend
)

# Define specific task routing
app.conf.task_routes = {
    "worker_tasks.generate_blog_task": {"queue": "blog"},
}
