from celery import Celery

# Define the Celery app
app = Celery(
    "workers",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@app.task
def generate_blog_task(prompt):
    # Add your blog generation logic here
    return f"Blog content for prompt: {prompt}"
