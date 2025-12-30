import requests
from bs4 import BeautifulSoup

def load_job_description(url=None, text=None):
    if text:
        return text.strip()

    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator="\n").strip()
