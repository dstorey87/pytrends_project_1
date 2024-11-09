import os
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set paths and model name
model_name = "EleutherAI/gpt-j-6B"  # Change this if using a different model
model_cache_dir = r"F:\models\gpt-j-6b"
offload_folder = r"F:\models\offload_weights"  # Specify folder for offloaded weights

# Ensure required directories exist
os.makedirs(model_cache_dir, exist_ok=True)
os.makedirs(offload_folder, exist_ok=True)

print("Starting download and initialization of GPT-J-6B for CPU with offload support...")

# Download and initialize the model with offload support
try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",  # Automatically map devices
        torch_dtype="float32",  # Use float32 precision for CPU
        cache_dir=model_cache_dir,
        offload_folder=offload_folder  # Specify offload folder
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=model_cache_dir
    )
    print("Model and tokenizer downloaded and initialized successfully.")
except Exception as e:
    print(f"Error initializing model: {e}")
    raise
