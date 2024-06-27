/* 
    ## En este script se maneja la información recolectada de una base de datos de los hoteles,
    ## esto con el fin de generar cartas en el index y también rellenar la página de
    ## 'infoHoteles.html' con la información en cuestión de cada hotel de manera dinamica.

*/

/* --- RECOLECTAR DATOS DE LA BD E IMPRIMIR CARDS DE MANERA DINAMICA --- */
document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');
    const navLinks = document.querySelectorAll('.nav-link');

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
        card.classList.add('col-md-3', 'mb-4');

        let precioDescuento = `<h4 class="card-title">${formatearPrecio(hotel.precio)}</h4>`;
        if (hotel.en_oferta && hotel.porcentaje_descuento > 0) {
            precioDescuento = `
                <h4 class="card-title text-danger">${formatearPrecio(hotel.precio_con_descuento)}</h4>
                <p class="text-muted"><s>${formatearPrecio(hotel.precio)}</s></p>
                <span class="badge bg-danger">${hotel.porcentaje_descuento}% OFF</span>
            `;
        }

        card.innerHTML = `
            <div class="card" id="cartasInicio">
                <img src="/media/${hotel.foto}" class="card-img-top" alt="Imagen Hotel">
                <div class="card-body">
                    ${precioDescuento}
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

        const botonVerMas = card.querySelector('.ver-mas-info');
        botonVerMas.addEventListener('click', () => {
            localStorage.setItem('hotelSeleccionado', JSON.stringify(hotel));
            window.location.href = '/informacion-hotel/';
        });

        // Configuración para las tarjetas de los hoteles en "index.html"
        const nuevaCard = card.querySelector('.card');

        // Aplica los estilos a la imagen principal (card-img-top) dentro de la tarjeta
        const imagen = nuevaCard.querySelector('.card-img-top');
        imagen.style.width = '400px';
        imagen.style.height = '600px';
        imagen.style.display = 'block';
        imagen.style.margin = '0 auto';
    
        // Aplica los estilos al cuerpo de la tarjeta (card-body) dentro de la tarjeta
        const cuerpoTarjeta = nuevaCard.querySelector('.card-body');
        cuerpoTarjeta.style.display = 'flex';
        cuerpoTarjeta.style.flexDirection = 'column';
        cuerpoTarjeta.style.justifyContent = 'center';
        cuerpoTarjeta.style.height = '100%'; // Ajusta la altura del contenedor del cuerpo de la carta

        return card;
    }

        // Función para obtener y mostrar los hoteles filtrados
        function obtenerHoteles(filtro = '') {
            let url = '/api/hoteles/';
            if (filtro) {
                url += `?${filtro}`;
            }
    
            fetch(url)
                .then(response => response.json())
                .then(hoteles => {
                    hotelesContainer.innerHTML = '';
                    hoteles.forEach(hotel => {
                        const card = crearCardProducto(hotel);
                        hotelesContainer.appendChild(card);
                    });
                })
                .catch(error => console.error('Error al obtener los datos de los hoteles:', error));
        }
    
        // Event listener para los filtros del navbar usando un switch
        navLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const filtro = link.getAttribute('data-filtro');
                switch (filtro) {
                    case 'ofertas':
                        obtenerHoteles('en_oferta=true');
                        break;
                    case 'todos':
                        obtenerHoteles();
                        break;
                    case 'frente_al_mar':
                        obtenerHoteles('categoria=frente_al_mar');
                        break;
                    case 'cabanas':
                        obtenerHoteles('categoria=cabanas');
                        break;
                    default:
                        obtenerHoteles();
                        break;
                }
            });
        });
        
    // Cargar todos los hoteles por defecto
    obtenerHoteles();
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