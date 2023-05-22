const themeSwitchCheckbox = document.getElementById('theme-switch-checkbox');
const body = document.body;

themeSwitchCheckbox.addEventListener('change', function () {
  body.classList.toggle('dark-theme');
});
