from celery import Celery

app = Celery(
    "worker_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

app.conf.task_routes = {
    "worker_tasks.generate_blog_task": {"queue": "blog_generation"}
}
