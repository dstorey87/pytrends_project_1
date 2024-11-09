import requests

def test_model_server():
    url = "http://127.0.0.1:5000/generate"
    prompt = {"prompt": "What is the impact of AI on society?"}
    
    try:
        response = requests.post(url, json=prompt)
        response.raise_for_status()
        print("Server response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model_server()
