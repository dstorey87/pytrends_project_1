# test_model_loading.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = r"F:\models\t5-3b\models--google--t5-v1_1-large\snapshots\a98b0fcd0b8137ded40cdf0c0cf0ee884e7c9726"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
