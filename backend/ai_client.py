import os
import json
from dotenv import load_dotenv
import openai
from openai.error import OpenAIError, RateLimitError

# Carrega variáveis de ambiente do .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    # Se não tiver chave, seguimos só com o fallback
    print("AVISO: OPENAI_API_KEY não definida. Usando apenas classificação local.")


def rule_based_fallback(cleaned_text: str) -> dict:
    """
    Classificação simplificada SEM chamar API externa.
    Usa palavras-chave para decidir Produtivo / Improdutivo
    e monta uma resposta padrão.
    """

    text = cleaned_text.lower()

    # Palavras que indicam email produtivo (pedindo algo, problema etc.)
    productive_keywords = [
        "status", "limite", "cartão", "fatura", "boleto", "cobrança",
        "suporte", "erro", "problema", "reclamação", "cancelamento",
        "atendimento", "prazo", "solicitação", "chamado", "ajuda",
        "débito", "crédito", "conta", "transação", "estorno"
    ]

    is_productive = any(word in text for word in productive_keywords)

    if is_productive:
        category = "Produtivo"
        confidence = 0.75
        reply = (
            "Olá! Obrigado pelo seu contato.\n\n"
            "Identificamos que sua mensagem requer análise da equipe. "
            "Seu pedido será encaminhado para o setor responsável e você receberá um retorno em breve. "
            "Se possível, envie também dados complementares (CPF, número do cartão ou protocolo), "
            "sempre respeitando os canais oficiais e seguros da empresa.\n\n"
            "Atenciosamente,\nEquipe de Atendimento."
        )
    else:
        category = "Improdutivo"
        confidence = 0.7
        reply = (
            "Olá! Agradecemos muito sua mensagem e sua consideração.\n\n"
            "Ficamos felizes com o seu contato. Caso precise de qualquer suporte ou tenha alguma dúvida "
            "sobre nossos produtos ou serviços, estamos à disposição pelos canais oficiais.\n\n"
            "Atenciosamente,\nEquipe de Atendimento."
        )

    return {
        "category": category,
        "confidence": confidence,
        "reply": reply
    }


def analyze_email_with_ai(cleaned_text: str) -> dict:
    """
    Tenta usar a API da OpenAI.
    Se não conseguir (quota, erro de rede, falta de chave etc.),
    usa o fallback local rule-based.
    """

    if not cleaned_text or len(cleaned_text.strip()) == 0:
        return {
            "category": "Improdutivo",
            "confidence": 0.5,
            "reply": "Não foi possível identificar o conteúdo do email."
        }

    # Se não tiver chave de API, já cai direto no fallback
    if not OPENAI_API_KEY:
        print("Sem OPENAI_API_KEY. Usando fallback local.")
        return rule_based_fallback(cleaned_text)

    prompt = f"""
Você é um assistente de uma empresa do setor financeiro.

Você receberá o texto de um email de um cliente e deve:

1. Classificar o email em UMA das categorias:
   - Produtivo: requer ação, resposta ou acompanhamento da equipe.
   - Improdutivo: não requer ação (felicitações, agradecimentos simples, mensagens genéricas).

2. Gerar uma resposta profissional, em português, de acordo com a categoria:
   - Se PRODUTIVO: responda de forma cordial, peça dados importantes se necessário,
     reconheça a solicitação e indique próximo passo (ex.: prazo de retorno, encaminhamento ao setor responsável, etc.).
   - Se IMPRODUTIVO: responda de forma educada, agradecendo a mensagem e encerrando cordialmente.

IMPORTANTE: responda APENAS com um JSON válido neste formato exato:

{{
  "category": "Produtivo" ou "Improdutivo",
  "confidence": número entre 0 e 1,
  "reply": "texto da resposta em português"
}}

Texto do email:
\"\"\"{cleaned_text}\"\"\"
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        text = completion.choices[0].message["content"]

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Se não respeitar o JSON, tratamos como produtivo com a própria resposta
            return {
                "category": "Produtivo",
                "confidence": 0.8,
                "reply": text.strip()
            }

        category = data.get("category", "Produtivo")
        confidence = float(data.get("confidence", 0.9))
        reply = data.get("reply", "")

        return {
            "category": category,
            "confidence": confidence,
            "reply": reply
        }

    except RateLimitError as e:
        # Sem quota / limite excedido → fallback local
        print(f"RateLimitError na OpenAI: {e}. Usando fallback local.")
        return rule_based_fallback(cleaned_text)

    except OpenAIError as e:
        # Qualquer outro erro da API → fallback local
        print(f"OpenAIError: {e}. Usando fallback local.")
        return rule_based_fallback(cleaned_text)

    except Exception as e:
        # Erro inesperado → também não derruba a API
        print(f"Erro inesperado ao chamar IA: {e}. Usando fallback local.")
        return rule_based_fallback(cleaned_text)
