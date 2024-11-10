from worker_tasks import generate_blog_task

# Trigger the task
result = generate_blog_task.delay("Write a detailed blog about AI's impact on society.")

# Print task details
print("Task status:", result.status)
try:
    print("Task result:", result.get(timeout=30))  # Wait for 30 seconds for the result
except Exception as e:
    print("Error:", str(e))
