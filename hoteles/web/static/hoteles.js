/* 
    ## En este script se maneja la información recolectada de una base de datos de los hoteles,
    ## esto con el fin de generar cartas en el index y también rellenar la página de
    ## 'infoHoteles.html' con la información en cuestión de cada hotel de manera dinamica.

*/

/* --- BASE DE DATOS LOCAL --- */
const hoteles = [
    // Agregar hoteles
    { 
        id: 1, 
        nombre: 'Nombre Hotel', 
        descripcionBreve: 'Descripción breve hotel',
        descripcionDetallada: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel placeat delectus ut accusamus, impedit autem! Amet voluptates rerum labore ab, molestias et libero dolores inventore exercitationem minima optio, at praesentium!',
        precio: 529990
    },
    { 
        id: 2, 
        nombre: 'Nombre Hotel', 
        descripcionBreve: 'Descripción breve hotel',
        descripcionDetallada: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel placeat delectus ut accusamus, impedit autem! Amet voluptates rerum labore ab, molestias et libero dolores inventore exercitationem minima optio, at praesentium!',
        precio: 779990 
    },
    { 
        id: 3, 
        nombre: 'Nombre Hotel', 
        descripcionBreve: 'Descripción breve hotel',
        descripcionDetallada: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel placeat delectus ut accusamus, impedit autem! Amet voluptates rerum labore ab, molestias et libero dolores inventore exercitationem minima optio, at praesentium!',
        precio: 332488 },
    { 
        id: 4, 
        nombre: 'Nombre Hotel', 
        descripcionBreve: 'Descripción breve hotel',
        descripcionDetallada: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Vel placeat delectus ut accusamus, impedit autem! Amet voluptates rerum labore ab, molestias et libero dolores inventore exercitationem minima optio, at praesentium!',
        precio: 14315 
    },
];

/* --- GESTIÓN DE CARTAS DINAMICAS --- */
document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');

    hoteles.forEach(hotel => {
        const card = crearCardProducto(hotel);
        hotelesContainer.appendChild(card);
    });

    // Función para formatear el precio en pesos chilenos (CLP)
    function formatearPrecio(precio) {
        const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        });
        return formatter.format(precio);
    }

    // Función encargada de crear y modificar las cartas de los hoteles
    function crearCardProducto(hotel) {
        const card = document.createElement('div');
        // Modificar carta/s
        card.classList.add('col-md-3', 'mb-4');

        card.innerHTML = `
            <div class="card" id="cartasInicio">
                <img src="..." class="card-img-top" alt="Imagen Hotel">
                <div class="card-body">
                    <h4 class="card-title">${formatearPrecio(hotel.precio)}</h4>
                    <p class="card-title">${hotel.nombre}</p>
                    <p class="card-text">${hotel.descripcionBreve}</p>
                    <button 
                        class="btn btn-primary ver-mas-info" 
                        data-id="${hotel.id}" 
                        data-nombre="${hotel.nombre}"
                        data-precio="${hotel.precio}"
                        >
                        Ver más información / Reservar
                    </button>
                </div>
            </div>
        `;

        // Configuración para las tarjetas de los hoteles en "index.html"
        const nuevaCard = card.querySelector('.card');

        // Aplica los estilos a la imagen principal (card-img-top) dentro de la tarjeta
        const imagen = nuevaCard.querySelector('.card-img-top');
        imagen.style.width = '100%';
        imagen.style.maxWidth = '200px';
        imagen.style.height = 'auto';
        imagen.style.display = 'block';
        imagen.style.margin = '0 auto';
    
        // Aplica los estilos al cuerpo de la tarjeta (card-body) dentro de la tarjeta
        const cuerpoTarjeta = nuevaCard.querySelector('.card-body');
        cuerpoTarjeta.style.display = 'flex';
        cuerpoTarjeta.style.flexDirection = 'column';
        cuerpoTarjeta.style.justifyContent = 'center';
        cuerpoTarjeta.style.height = '100%'; // Ajusta la altura del contenedor del cuerpo de la carta

        // Añadir evento al botón para redireccionar a la página con info más detalla del hotel seleccionado
        const botonVerMas = card.querySelector('.ver-mas-info');
        botonVerMas.addEventListener('click', () => {
            localStorage.setItem('hotelSeleccionado', JSON.stringify(hotel));
            window.location.href = '/informacion-hotel/';
        });

        return card;
    }
});

/* --- GESTIÓN DE MANEJO DE INFORMACIÓN POR HOTEL --- */
document.addEventListener('DOMContentLoaded', () => {
    const hotelInfoContainer = document.getElementById('hotel-info');
    const hotelSeleccionado = JSON.parse(localStorage.getItem('hotelSeleccionado'));

    if (hotelSeleccionado) {
        hotelInfoContainer.innerHTML = `
            <h1>${hotelSeleccionado.nombre}</h1>
            <p><strong>Precio: </strong>${new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(hotelSeleccionado.precio)}</p>
            <p><strong>Descripción detallada: </strong>${hotelSeleccionado.descripcionDetallada}</p>
        `;
    } else {
        hotelInfoContainer.innerHTML = '<p>No se encontró información del hotel seleccionado.</p>';
    }
});