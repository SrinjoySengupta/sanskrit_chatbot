function normalize(text) {
  return text.toLowerCase().replace(/[^\w\s]/gi, '').trim();
}
function fuzzyMatch(input) {
  const normalizedInput = normalize(input);
  let bestMatch = null;
  let minDistance = Infinity;

  for (const key in QA_PAIRS) {
    const dist = levenshtein(normalize(key), normalizedInput);
    if (dist < minDistance) {
      minDistance = dist;
      bestMatch = key;
    }
  }
  return minDistance <= 3
    ? QA_PAIRS[bestMatch]
    : "क्षम्यताम्। मम कृते तस्य प्रश्नस्य उत्तरं उपलब्धं नास्ति। कृपया अन्यथा पृच्छतु।";
}
function levenshtein(a, b) {
  const matrix = Array.from({ length: a.length + 1 }, () => []);
  for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  return matrix[a.length][b.length];
}
function sendMessage() {
  const inputField = document.getElementById("userInput");
  const input = inputField.value.trim();
  if (input === "") return;

  appendMessage("user", input);
  const response = fuzzyMatch(input);
  setTimeout(() => appendMessage("bot", response), 500);
  inputField.value = "";
}
function appendMessage(sender, message) {
  const chat = document.getElementById("chatContainer");
  const msg = document.createElement("div");
  msg.className = `chat-message ${sender}`;
  msg.innerHTML = sender === "user"
    ? `🙋‍♂️ <strong>You:</strong> ${message}`
    : `🕉️ <strong>Bot:</strong> ${message}`;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}
function attachChatEvents() {
  document.getElementById("sendBtn").addEventListener("click", sendMessage);
  document.getElementById("userInput").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });
}
attachChatEvents();