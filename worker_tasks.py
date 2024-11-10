from celery import Celery

# Initialize Celery application
app = Celery('worker_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def generate_blog_task(prompt):
    return f"Blog generated for prompt: {prompt}"
