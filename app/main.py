from app.jd_loader import load_job_description
from app.resume_parser import extract_resume_text
from app.ollama_client import generate
from app.markdown_to_pdf import markdown_to_pdf
from app.utils import create_output_folder

def run_pipeline(job_url, resume_pdf, company, role):
    jd = load_job_description(job_url)
    resume_text = extract_resume_text(resume_pdf)

    with open("prompts/resume_prompt.txt") as f:
        r_prompt = f.read()

    with open("prompts/cover_letter_prompt.txt") as f:
        c_prompt = f.read()

    resume_md = generate(
        r_prompt.replace("{{JOB_DESCRIPTION}}", jd)
                .replace("{{RESUME_TEXT}}", resume_text)
    )

    cover_md = generate(
        c_prompt.replace("{{JOB_DESCRIPTION}}", jd)
                .replace("{{RESUME_TEXT}}", resume_text)
                .replace("{{COMPANY}}", company)
                .replace("{{ROLE}}", role)
    )

    out = create_output_folder()
    markdown_to_pdf(resume_md, f"{out}/Resume.pdf")
    markdown_to_pdf(cover_md, f"{out}/Cover_Letter.pdf")

    return out
