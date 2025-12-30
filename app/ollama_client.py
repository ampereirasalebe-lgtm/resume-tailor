import requests

def generate(prompt, model="deepseek-r1:latest"):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    r.raise_for_status()
    return r.json()["response"]
