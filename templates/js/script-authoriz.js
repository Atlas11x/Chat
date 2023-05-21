var settingsIcon = document.querySelector('.settings-icon');
var dropdownMenu = document.querySelector('.dropdown-menu');

settingsIcon.addEventListener('click', function() {
  dropdownMenu.classList.toggle('show');
});

function changeColor(color) {
  document.body.style.backgroundColor = color;
}
