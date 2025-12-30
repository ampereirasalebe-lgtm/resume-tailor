from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.main import run_pipeline
import shutil, os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
os.makedirs("resumes", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    job_url: str = Form(...),
    company: str = Form(...),
    role: str = Form(...),
    resume: UploadFile = File(...)
):
    path = f"resumes/{resume.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    out = run_pipeline(job_url, path, company, role)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"Generated in: {out}"
    })
