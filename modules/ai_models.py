# File: modules/ai_models.py

import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def initialize_generator(model_path, offload_folder=None):
    """
    Initialize the language generation model.

    Args:
        model_path (str): Path to the model or Hugging Face model identifier.
        offload_folder (str, optional): Directory for offloading model weights to disk.

    Returns:
        model: Initialized model instance or None if initialization failed.
    """
    try:
        logging.info(f"Starting download and initialization of model from {model_path}...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Pass `offload_folder` if specified, else use defaults for loading
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            offload_folder=offload_folder if offload_folder else None
        )
        
        logging.info("Model and tokenizer downloaded and initialized successfully.")
        return model
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        return None

def generate_blog_content(generator, prompt):
    """
    Generate blog content based on the given prompt.
    """
    try:
        model = generator["model"]
        tokenizer = generator["tokenizer"]
        device = generator["device"]

        # Tokenize input prompt
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

        # Generate content
        outputs = model.generate(
            input_ids,
            max_length=512,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
        )
        blog_content = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logging.info("Blog content generated successfully.")
        return blog_content
    except Exception as e:
        logging.error(f"Error generating blog content: {e}")
        return None
