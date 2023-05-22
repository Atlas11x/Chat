var toggleIcon = document.querySelector('.toggle-icon');
var colorWave = document.querySelector('.color-wave');
var colorList = document.querySelector('.color-list');
var submitButton = document.querySelector('input[type="submit"]');

toggleIcon.addEventListener('click', function() {
  colorList.style.display = colorList.style.display === 'none' ? 'block' : 'none';
});

colorList.addEventListener('click', function(event) {
  var color = event.target.dataset.color;
  if (color) {
    changeColor(color);
    colorList.style.display = 'none';
  }
});

function changeColor(color) {
  submitButton.style.backgroundColor = color;
  colorWave.style.opacity = 1;
  colorWave.style.backgroundImage = `linear-gradient(to right, #03e9f4, ${color}, #ffeb3b)`;

  setTimeout(function() {
    colorWave.style.opacity = 0;
    submitButton.classList.add('neon');
    setTimeout(function() {
      submitButton.classList.remove('neon');
    }, 1000);
  }, 2000);
}
