document.addEventListener("DOMContentLoaded", () => {
  const kycForm = document.getElementById("kycForm");
  if (!kycForm) return;

  kycForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const roll = document.getElementById("roll").value.trim();
    const email = document.getElementById("email").value.trim();

    sessionStorage.setItem("name", name);
    sessionStorage.setItem("roll", roll);
    sessionStorage.setItem("email", email);

    window.location.href = "chatbot.html";
  });
});