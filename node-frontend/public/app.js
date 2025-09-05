const API_URL = "/api/messages";

async function loadMessages() {
  const res = await fetch(API_URL);
  const data = await res.json();
  const list = document.getElementById("messages");
  list.innerHTML = "";
  data.forEach(m => {
    const li = document.createElement("li");
    li.textContent = m.text + " (" + new Date(m.created_at).toLocaleString() + ")";
    list.appendChild(li);
  });
}

document.getElementById("msgForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("msgInput").value;
  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  document.getElementById("msgInput").value = "";
  loadMessages();
});

loadMessages();
