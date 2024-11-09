from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to the GPT-J-6B model
model_path = r"F:\models\gpt-j-6b\models--EleutherAI--gpt-j-6B\snapshots\47e169305d2e8376be1d31e765533382721b2cc1"

# Load the tokenizer and model
print("Loading GPT-J-6B model...")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Flask app setup
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get the input text from the POST request
        data = request.json
        input_text = data.get("text", "")

        # Tokenize the input
        inputs = tokenizer(input_text, return_tensors="pt")

        # Generate a response
        outputs = model.generate(inputs["input_ids"], max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the response
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting GPT-J-6B server...")
    app.run(host='0.0.0.0', port=5000)
