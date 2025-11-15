from fastapi import UploadFile
import PyPDF2
from io import BytesIO

async def extract_text_from_uploadfile(file: UploadFile) -> str:
    """
    Lê o conteúdo de um UploadFile (.txt ou .pdf) e retorna texto.
    """
    content = await file.read()
    filename = (file.filename or "").lower()

    # TXT
    if filename.endswith(".txt"):
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")

    # PDF
    if filename.endswith(".pdf"):
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception:
            pass
        return text

    # Tipo não suportado
    return ""
