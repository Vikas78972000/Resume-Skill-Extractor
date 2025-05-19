from fastapi import APIRouter, UploadFile, File, HTTPException
import io

from PyPDF2 import PdfReader
import docx

router = APIRouter()


KEYWORDS = [
    "Python", "Java", "C++", "JavaScript", "React", "Angular", "Node.js", "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "FastAPI", "Flask", "Django", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Git", "CI/CD", "HTML", "CSS", "Tailwind", "Bootstrap", "TensorFlow", "PyTorch", "Pandas",
    "NumPy", "Data Analysis", "Machine Learning", "Deep Learning", "NLP", "Linux", "Agile", "Scrum"
]

@router.post("/extract-skills")
async def extract_skills(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = ""

        # Detect file type
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(content)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(content)
        elif file.filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text:
            raise HTTPException(status_code=422, detail="Failed to extract text from file")

        # ✅ Extract skills
        skills = [word for word in KEYWORDS if word.lower() in text.lower()]
        return {"skills": skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def extract_text_from_pdf(pdf_bytes):
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception:
        return ""


def extract_text_from_docx(docx_bytes):
    try:
        doc = docx.Document(io.BytesIO(docx_bytes))
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception:
        return ""
