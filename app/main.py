
from app.jd_loader import load_job_description
from app.ollama_client import generate
from app.markdown_to_pdf import markdown_to_pdf
from app.utils import create_output_folder
from app.resume_parser import (
    extract_resume_text,
    extract_resumes_from_folder
)

def run_pipeline(job_url, resume_pdf, company, role):
    jd = load_job_description(job_url)
    safe_company = company if company else "the organization"
    safe_role = role if role else "this role"
    if resume_pdf:
        resume_text = extract_resume_text(resume_pdf)
    else:
        resume_text = extract_resumes_from_folder("resumes")

    with open("prompts/resume_prompt.txt") as f:
        resume_prompt = f.read()

    with open("prompts/cover_letter_prompt.txt") as f:
        cover_prompt = f.read()

    resume_md = generate(
        resume_prompt
        .replace("{{JOB_DESCRIPTION}}", jd)
        .replace("{{RESUME_TEXT}}", resume_text)
    )

    cover_md = generate(
        cover_prompt
        .replace("{{JOB_DESCRIPTION}}", jd)
        .replace("{{RESUME_TEXT}}", resume_text)
        .replace("{{COMPANY}}", safe_company)
        .replace("{{ROLE}}", safe_role)
    )

    out_dir = create_output_folder()
    markdown_to_pdf(resume_md, f"{out_dir}/Resume.pdf")
    markdown_to_pdf(cover_md, f"{out_dir}/Cover_Letter.pdf")

    return out_dir
