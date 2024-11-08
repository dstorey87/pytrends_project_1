import logging
from transformers import AutoTokenizer, GPTJForCausalLM
import torch
from bitsandbytes.optim import GlobalOptimManager

def initialize_generator(model_path, quantize=False):
    """
    Initialize the language generation model and tokenizer from a local directory.

    Args:
        model_path (str): Path to the local model directory.
        quantize (bool): Whether to enable quantization for the model.

    Returns:
        dict: Dictionary containing the tokenizer and model.
    """
    try:
        logging.info(f"Loading model and tokenizer from '{model_path}'.")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Conditional quantized model loading
        if quantize:
            logging.info("Using quantized model loading.")
            model = GPTJForCausalLM.from_pretrained(
                model_path,
                load_in_8bit=True,  # Enable 8-bit precision
                device_map="auto",  # Automatically map to available devices
            )
        else:
            logging.info("Loading full-precision model.")
            model = GPTJForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            )
        
        # Move model to device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        logging.info("Generator model initialized successfully.")
        return {"tokenizer": tokenizer, "model": model, "device": device}
    except Exception as e:
        logging.error(f"Error initializing generator model: {e}")
        return None


def generate_blog_content(generator, prompt, max_length=1024):
    """
    Generate blog content based on the prompt using the language generation model.

    Args:
        generator (dict): Dictionary containing the tokenizer, model, and device.
        prompt (str): The prompt to generate content from.
        max_length (int): Maximum length of the generated content.

    Returns:
        str: Generated blog content.
    """
    try:
        tokenizer = generator["tokenizer"]
        model = generator["model"]
        device = generator["device"]

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        max_model_length = model.config.n_positions
        adjusted_max_length = min(max_length, max_model_length)

        outputs = model.generate(
            **inputs,
            max_length=adjusted_max_length,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id
        )
        content = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return content
    except Exception as e:
        logging.error(f"Error generating blog content: {e}")
        return None
