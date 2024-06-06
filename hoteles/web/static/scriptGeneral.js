/* 
    ## Este es el scrip general para manejar cosas como mantener los botones activos,
    ## funciones pequeñas, cambiar imagenes a conveniencia, mostrar modales, entre otros.

    ## Para hacer cosas más detalladas como, por ejemplo, gestionar un carrito de compras y
    ## todo eso, se utilizarán .js especificos para ello. Este namás es para tonteras chicas.
*/

document.addEventListener('DOMContentLoaded', function () {
    const registrateLink = document.getElementById('registrate');
    const modalRegistro = new bootstrap.Modal(document.getElementById('modalRegistro'));
    const iniciarSesionLink = document.getElementById('iniciarSesion');
    const modalIniciarSesion = new bootstrap.Modal(document.getElementById('modalIniciarSesion'));

    // Muestra el modal de registro al hacer clic en "Regístrate"
    registrateLink.addEventListener('click', function (event) {
        event.preventDefault();
        modalRegistro.show();
    });
    // Muestra el modal de inicio de sesión al hacer clic en "Iniciar sesión"
    iniciarSesionLink.addEventListener('click', function (event) {
        event.preventDefault();
        modalIniciarSesion.show();
    });

    function handleNavbarItems() {
        const navbarItems = document.querySelectorAll("#navbarNav .nav-item");
        const dropdownMenu = document.querySelector("#navbarDropdown .dropdown-menu");
        const navbarContainer = document.querySelector("#navbarNav .navbar-nav");
        const windowWidth = window.innerWidth;
    
        if (windowWidth < 768) {
            navbarItems.forEach(item => {
              dropdownMenu.appendChild(item);
            });
        } else {
            navbarItems.forEach(item => {
              navbarContainer.appendChild(item);
            });
        }
    }
    
    window.addEventListener("resize", handleNavbarItems);
    handleNavbarItems();
});