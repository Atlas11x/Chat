document.addEventListener("DOMContentLoaded", function() {
  const body = document.querySelector("body");
  const themeToggle = document.getElementById("theme-toggle");

  themeToggle.addEventListener("change", function() {
    if (this.checked) {
      body.classList.add("dark-theme");
    } else {
      body.classList.remove("dark-theme");
    }
  });
});
