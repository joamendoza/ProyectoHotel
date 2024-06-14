/* 
    ## En este script se maneja la información recolectada de una base de datos de los hoteles,
    ## esto con el fin de generar cartas en el index y también rellenar la página de
    ## 'infoHoteles.html' con la información en cuestión de cada hotel de manera dinamica.

*/

/* --- RECOLECTAR DATOS DE LA BD E IMPRIMIR CARDS DE MANERA DINAMICA --- */
document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');

    // Obtener los datos de los hoteles desde la API
    fetch('/api/hoteles/')
        .then(response => response.json())
        .then(data => {
            const hoteles = data;

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
                            <p class="card-text">${hotel.descripcion_breve}</p>
                            <button 
                                class="btn btn-primary ver-mas-info" 
                                data-id="${hotel.id}" 
                                data-nombre="${hotel.nombre}"
                                data-precio="${hotel.precio}"
                                >
                                Ver más información
                            </button>
                        </div>
                    </div>
                `;

                 // Configuración para las tarjetas de los hoteles en "index.html"
                const nuevaCard = card.querySelector('.card');

                // Aplica los estilos a la imagen principal (card-img-top) dentro de la tarjeta
                const imagen = nuevaCard.querySelector('.card-img-top');
                imagen.style.width = '400px';
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
        })
        .catch(error => console.error('Error al obtener los datos de los hoteles:', error));
});

/* --- GESTIÓN DE MANEJO DE INFORMACIÓN POR HOTEL --- */
document.addEventListener('DOMContentLoaded', () => {
    const hotelInfoContainer = document.getElementById('hotel-info');
    const hotelSeleccionado = JSON.parse(localStorage.getItem('hotelSeleccionado'));

    if (hotelSeleccionado) {
        hotelInfoContainer.innerHTML = `
            <div class="card mb-3" style="width: 940px;">
                <div class="row g-0">
                    <div class="col-md-4">
                        <img src="/media/${hotelSeleccionado.foto}" class="img-fluid rounded-start" alt="Imagen hotel">
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">${hotelSeleccionado.nombre}</h5>
                            <p class="card-text">Precio por noche: ${new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(hotelSeleccionado.precio)}</p>
                            <br>
                            <p class="card-text">${hotelSeleccionado.descripcion_detallada}</p>
                        </div>   
                    </div>
                </div>
            </div>
        `;
    } else {
        hotelInfoContainer.innerHTML = '<p>No se encontró información del hotel seleccionado.</p>';
    }
});