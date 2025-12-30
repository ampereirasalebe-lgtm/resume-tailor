import requests

""" 
deepseek-r1:latest
gpt-oss-safeguard:20b
llama3.1:8b 
"""

def generate(prompt, model="deepseek-r1:latest"):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    r.raise_for_status()
    return r.json()["response"]
