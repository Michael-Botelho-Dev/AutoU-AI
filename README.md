# Classificador de E-mails com IA – AutoU Challenge

Aplicação web que lê o conteúdo de e-mails, **classifica como Produtivo ou Improdutivo** e **gera uma resposta automática sugerida**, usando inteligência artificial e regras de negócio simples.

Projeto desenvolvido como parte de um desafio técnico para uma empresa do setor financeiro.

---

## 🧠 Objetivo

Automatizar a triagem de e-mails recebidos por uma equipe de atendimento:

- **Produtivo** → e-mails que exigem análise, ação ou resposta (ex.: status de solicitação, problemas com fatura, dúvidas sobre produtos/serviços).
- **Improdutivo** → e-mails que não exigem ação imediata (ex.: felicitações, agradecimentos simples).

A solução:

- Lê o texto do e-mail (via texto colado ou upload de `.txt` / `.pdf`)
- Classifica o e-mail
- Sugere uma resposta automática adequada ao tipo de e-mail

---

## 🏗️ Arquitetura da Solução

A aplicação é dividida em dois módulos principais:

### 1. Backend (API em Python + FastAPI)

Responsável por:

- Receber o conteúdo do e-mail (texto ou arquivo)
- Extrair texto de arquivos `.txt` e `.pdf`
- Fazer pré-processamento básico de NLP
- Classificar o e-mail
- Gerar a resposta sugerida

Principais arquivos:

- `backend/main.py`  
  Define a API (`/analyze-email`) e realiza o fluxo geral:
  - recebe o formulário
  - extrai o texto
  - pré-processa
  - chama a camada de IA
  - retorna JSON com `category`, `confidence`, `reply`

- `backend/nlp.py`  
  Tratamento básico do texto:
  - normalização para minúsculas
  - remoção de caracteres especiais
  - normalização de espaços

- `backend/utils.py`  
  Funções utilitárias, incluindo:
  - leitura de arquivos `.txt`
  - extração de texto de `.pdf` usando `PyPDF2`

- `backend/ai_client.py`  
  Camada de IA e regras de fallback:
  - tenta chamar a API da OpenAI (`gpt-3.5-turbo`)
  - se não houver chave, quota ou houver erro na API, usa um **classificador local por palavras-chave**
  - sempre retorna um dicionário com:
    - `category`: `"Produtivo"` ou `"Improdutivo"`
    - `confidence`: número entre 0 e 1
    - `reply`: texto da resposta sugerida em português

### 2. Frontend (HTML + CSS + JavaScript puro)

Interface simples, intuitiva e responsiva, com:

- Campo de texto para colar o conteúdo do e-mail
- Upload de arquivo `.txt` ou `.pdf`
- Botão **“Classificar Email”**
- Exibição de:
  - categoria resultante
  - confiança
  - resposta sugerida pela IA

Arquivos:

- `frontend/index.html` – estrutura da página
- `frontend/style.css` – estilo da interface
- `frontend/script.js` – integração com a API

---

## 🧩 Fluxo de Funcionamento

1. Usuário acessa a interface web.
2. Informa o e-mail:
   - colando o texto no campo, ou
   - fazendo upload de `.txt` ou `.pdf`.
3. Clica em **Classificar Email**.
4. O frontend envia uma requisição `POST` para o backend (`/analyze-email`) usando `FormData`.
5. O backend:
   - lê o formulário
   - extrai o texto (arquivo ou texto direto)
   - pré-processa com `nlp.py`
   - chama `analyze_email_with_ai` (em `ai_client.py`)
   - retorna um JSON.
6. O frontend exibe na tela:
   - **Categoria**
   - **Confiança**
   - **Resposta sugerida** pronta para ser usada/adaptada pela equipe.

---

## 🛠️ Tecnologias Utilizadas

### Backend

- Python 3.x
- FastAPI
- Uvicorn
- PyPDF2
- python-dotenv
- openai (biblioteca oficial da OpenAI – versão 0.28.0)

### Frontend

- HTML5
- CSS3
- JavaScript (fetch API / FormData)

---

## 🚀 Como Rodar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
