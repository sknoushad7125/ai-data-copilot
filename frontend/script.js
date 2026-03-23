const BASE_URL = "http://127.0.0.1:8000";

function addMessage(text, type) {
    const chatBox = document.getElementById("chat-box");

    const msg = document.createElement("div");
    msg.className = `message ${type}`;
    msg.innerText = text;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("query");
    const query = input.value;

    if (!query) return;

    addMessage(query, "user");
    input.value = "";

    const res = await fetch(`${BASE_URL}/ask?query=${query}`);
    const data = await res.json();

    let reply = data.answer || JSON.stringify(data, null, 2);

    addMessage(reply, "bot");
}

function clearChat() {
    document.getElementById("chat-box").innerHTML = "";
}