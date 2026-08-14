function sendMessage() {
    let msg = document.getElementById("user-input").value;
    let lang = document.getElementById("language").value;

    fetch("/chatbot", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg, lang: lang})
    })
    .then(res => res.json())
    .then(data => {
        let chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += `<p><b>You:</b> ${msg}</p>`;
        chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
        document.getElementById("user-input").value = "";
    });
}
