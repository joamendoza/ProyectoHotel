function updateLogo() {
  const logoImg = document.getElementById('logoImg');
  if (window.innerWidth <= 768) {
    logoImg.src = '{% static "/imagenes/iconos/veraniumIcon.png" %}';
  } else {
    logoImg.src = '{% static "/imagenes/iconos/veranium.png" %}';
  }
}

// Llama a la función cuando la página se carga y cuando se redimensiona
window.addEventListener('load', updateLogo);
window.addEventListener('resize', updateLogo);