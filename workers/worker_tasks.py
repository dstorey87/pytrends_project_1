import logging
from .celery_config import app
from modules.data_processing import generate_blog_prompts
from modules.helpers import save_data

@app.task
def generate_blog_task(prompt, output_dir):
    """Generate a blog using the provided prompt."""
    try:
        logging.info(f"Generating blog for prompt: {prompt}")
        # Simulated generation (replace with model server call).
        content = f"Generated blog content for: {prompt}"
        filepath = os.path.join(output_dir, f"blog_{prompt[:10]}.txt")
        save_data(filepath, content)
    except Exception as e:
        logging.error(f"Failed to generate blog: {e}")
