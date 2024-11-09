from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging
import os

# Flask app initialization
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Model and tokenizer initialization
MODEL_PATH = r"F:\models\gpt-j-6b\models--EleutherAI--gpt-j-6B\snapshots\47e169305d2e8376be1d31e765533382721b2cc1"
OFFLOAD_FOLDER = r"F:\offload"  # Adjust this if using multiple SSDs later

try:
    logging.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, pad_token="[PAD]")
    logging.info("Tokenizer loaded successfully.")
    
    logging.info("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        device_map="auto",  # Automatically selects the best device (e.g., GPU, CPU)
        offload_folder=OFFLOAD_FOLDER,  # Offloads layers to disk for better performance
        torch_dtype=torch.float16,  # Use half-precision for faster inference on supported GPUs
        low_cpu_mem_usage=True  # Optimizes memory usage on initialization
    )
    model.config.pad_token_id = tokenizer.pad_token_id
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error initializing model or tokenizer: {e}", exc_info=True)
    raise SystemExit("Failed to initialize the model and tokenizer. Exiting.")

@app.route("/generate", methods=["POST"])
def generate_text():
    """Generate text from a given prompt."""
    try:
        # Parse the request JSON
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        prompt = data["prompt"]
        max_length = data.get("max_length", 100)  # Default max_length to 100 if not provided
        temperature = data.get("temperature", 0.7)  # Default temperature to 0.7 if not provided
        top_p = data.get("top_p", 0.9)  # Default top_p to 0.9 if not provided
        logging.info(f"Generating text for prompt: '{prompt}' with max_length={max_length}, temperature={temperature}, top_p={top_p}")

        # Generate text
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        inputs = {key: value.to(model.device) for key, value in inputs.items()}
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            do_sample=True,  # Enables sampling for variability
            temperature=temperature,  # Controls randomness
            top_p=top_p  # Nucleus sampling for better quality
        )
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        logging.info(f"Generated text: {generated_text}")

        return jsonify({"text": generated_text})
    except Exception as e:
        logging.error(f"Error during text generation: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask server
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting GPT-J-6B server on port {port}...")
    app.run(host="0.0.0.0", port=port)
