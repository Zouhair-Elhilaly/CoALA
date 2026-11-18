
import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b"


def test_ollama():
    payload = {
        "model": MODEL_NAME,
        "prompt": "Explain in one sentence what a Python function is.",
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        print("Ollama connection successful!")
        print("Model:", result.get("model"))
        print("\nQwen response:")
        print(result.get("response"))

    except urllib.error.URLError as error:
        print("Could not connect to Ollama:")
        print(error)

    except Exception as error:
        print("Test failed:")
        print(error)


if __name__ == "__main__":
    test_ollama()
