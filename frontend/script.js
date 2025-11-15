const form = document.getElementById("email-form");
const resultDiv = document.getElementById("result");
const categorySpan = document.getElementById("category");
const confidenceSpan = document.getElementById("confidence");
const replyP = document.getElementById("reply");

// Ajuste essa URL se o backend estiver em outro lugar (deploy)
const API_URL = "http://127.0.0.1:8000/analyze-email";

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const emailText = document.getElementById("email-text").value.trim();
  const emailFile = document.getElementById("email-file").files[0];

  if (!emailText && !emailFile) {
    alert("Por favor, informe o texto do email ou envie um arquivo.");
    return;
  }

  const formData = new FormData();
  if (emailText) {
    formData.append("email_text", emailText);
  }
  if (emailFile) {
    formData.append("file", emailFile);
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    categorySpan.textContent = data.category;
    confidenceSpan.textContent = (data.confidence * 100).toFixed(1) + "%";
    replyP.textContent = data.reply;

    resultDiv.classList.remove("hidden");
  } catch (err) {
    console.error(err);
    alert("Erro ao comunicar com a API. Verifique se o backend está rodando.");
  }
});
