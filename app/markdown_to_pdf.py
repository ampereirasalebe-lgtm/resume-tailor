import subprocess
import tempfile
import os

def markdown_to_pdf(md_text, output_pdf):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as f:
        f.write(md_text.encode())
        md = f.name

    subprocess.run(["pandoc", md, "-o", output_pdf, "-V", "geometry:a4paper,margin=1in"], check=True)
    os.unlink(md)
