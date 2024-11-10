from celery_config import app

@app.task
def generate_blog_task(prompt):
    """
    Task for generating a blog based on the prompt.
    """
    return f"Generated blog content for prompt: {prompt}"
