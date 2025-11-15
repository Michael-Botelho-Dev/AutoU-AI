import re

def preprocess_text(text: str) -> str:
    """
    Pré-processa o texto do email:
    - deixa tudo minúsculo
    - remove caracteres especiais
    - normaliza espaços
    """
    if not text:
        return ""

    # tudo minúsculo
    text = text.lower()

    # remove caracteres estranhos, mantendo letras, números, acentos e espaços
    text = re.sub(r"[^a-z0-9áéíóúâêôãõç\s]", " ", text)

    # remove espaços duplicados
    text = re.sub(r"\s+", " ", text).strip()

    return text
