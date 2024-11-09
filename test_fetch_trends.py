import requests

def test_model_server():
    """Test the model server with a simple prompt."""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/generate",
            json={"prompt": "Explain the importance of AI in modern society.", "max_length": 150}
        )
        response.raise_for_status()
        print("Server response:", response.json().get("text", "No response text"))
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the model server: {e}")


if __name__ == "__main__":
    test_model_server()
