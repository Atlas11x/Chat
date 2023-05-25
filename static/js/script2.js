document.querySelector(".chat-input button").addEventListener("click", function(e) {
  e.preventDefault();
  var input = document.querySelector(".chat-input input");
  var message = input.value.trim();
  
  if (message !== "") {
    var chatMessages = document.querySelector(".chat-messages");
    var newMessage = document.createElement("div");
    newMessage.textContent = message;
    newMessage.classList.add("message");
    chatMessages.appendChild(newMessage);
    input.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
document.addEventListener("DOMContentLoaded", function() {
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;

  themeToggle.addEventListener("change", function() {
    if (this.checked) {
      body.classList.add("dark-theme");
    } else {
      body.classList.remove("dark-theme");
    }
  });
});

