from celery import Celery

app = Celery(
    'workers',
    broker='redis://redis_worker:6379/0',  # Redis container alias in Docker Compose
    backend='redis://redis_worker:6379/0'  # Results in Redis
)

app.conf.task_routes = {
    'workers.generate_blog_task': {'queue': 'blog'},
}
