from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.main import run_pipeline
from app.jd_loader import load_job_description
from app.markdown_to_pdf import markdown_to_pdf
from pathlib import Path
import shutil, os
import requests
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    job_url: str = Form(...),
    company: Optional[str] = Form(None),
    role: Optional[str] = Form(None),

    resume: UploadFile = File(None),
    model: Optional[str] = Form(None)
):
    resume_path = None
    
    # ✅ Only save if an actual file was selected
    if resume is not None and resume.filename:
        resume_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)

    try:
        out_dir = run_pipeline(
            job_url=job_url,
            resume_pdf=resume_path,
            company=company,
            role=role,
            model=model
        )
        message = f"Generated successfully in: {out_dir}"

    except Exception as e:
        message = f"Error: {str(e)}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message
        }
    )

@app.post("/scrape")
async def scrape_only(
    job_url: str = Form(...)
):
    try:
        job_description = load_job_description(job_url)

        if not job_description:
            raise ValueError("Empty job description")

        return {
            "job_description": job_description
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to scrape job URL: {str(e)}"
        )

@app.post("/markdown-to-pdf")
async def markdown_2_pdf(
    markdown: str = Form(...),
    output_path: str = Form(...)
):
    try:
        output = Path(output_path)

        # If a directory is provided, default filename
        if output.suffix.lower() != ".pdf":
            output.mkdir(parents=True, exist_ok=True)
            output_pdf = output / "Resume.pdf"
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output_pdf = output

        markdown_to_pdf(markdown, f"{output}/Resume.pdf")

        return {
            "status": "success",
            "pdf_path": str(output_pdf)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.get("/models")
async def get_ollama_models():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=10
        )
        response.raise_for_status()

        models = [m["name"] for m in response.json().get("models", [])]

        return {
            "models": models
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Ollama models: {str(e)}"
        )

