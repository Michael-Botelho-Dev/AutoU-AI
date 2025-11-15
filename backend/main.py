from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from nlp import preprocess_text
from ai_client import analyze_email_with_ai
from utils import extract_text_from_uploadfile

app = FastAPI(
    title="Email Classifier AI",
    description="API para classificar emails (Produtivo / Improdutivo) e sugerir respostas automáticas.",
    version="1.0.0"
)

# CORS – libera o frontend falar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, trocar para o domínio do front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API de classificação de emails com IA está no ar."}


@app.post("/analyze-email")
async def analyze_email(request: Request):
    """
    Lê os dados do formulário manualmente:
    - email_text: texto direto
    - file: UploadFile OU string vazia (quando vem do Swagger sem arquivo)
    """
    form = await request.form()

    # Pode vir None, string vazia ou texto mesmo
    email_text = form.get("email_text") or ""
    file = form.get("file")  # pode ser UploadFile OU "" (string vazia)

    raw_text = ""

    # 1. Se veio arquivo de verdade, ele será um UploadFile
    if hasattr(file, "filename") and file.filename:
        raw_text = await extract_text_from_uploadfile(file)
    # 2. Senão, tenta usar o texto do campo
    elif email_text.strip():
        raw_text = email_text.strip()

    # 3. Se continuou vazio, retorna erro amigável
    if not raw_text:
        return {"error": "Envie um texto de email ou um arquivo (.txt ou .pdf)."}

    # 4. Pré-processar (NLP simples)
    cleaned_text = preprocess_text(raw_text)

    # 5. Chamar IA para classificar e gerar resposta
    result = analyze_email_with_ai(cleaned_text)

    return {
        "original_text": raw_text,
        "cleaned_text": cleaned_text,
        "category": result["category"],
        "confidence": result["confidence"],
        "reply": result["reply"]
    }
