from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.main import run_pipeline
import shutil, os
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

    resume: UploadFile = File(None)
):
    resume_path = None
    #test
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
            role=role
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
