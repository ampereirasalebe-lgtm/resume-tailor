from datetime import datetime
import os

def create_output_folder(base="output"):
    name = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = os.path.join(base, name)
    os.makedirs(path, exist_ok=True)
    return path
