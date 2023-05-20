var chatbox = document.getElementById("chatbox");
var messageInput = document.getElementById("message");

function sendMessage() {
    var message = messageInput.value;

    if (message !== "") {
        var newMessage = document.createElement("p");
        newMessage.innerText = "Me: " + message;
        newMessage.classList.add("sent-message"); // Add a class for styling
        chatbox.appendChild(newMessage);
        messageInput.value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}
