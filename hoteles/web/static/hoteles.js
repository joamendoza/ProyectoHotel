document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');

    const hoteles = [
        // Agrega hoteles
        { id: 1, nombre: 'Nombre Hotel', descripcion: 'Descripción hotel', precio: 529990 },
        { id: 2, nombre: 'Nombre Hotel', descripcion: 'Descripción hotel', precio: 779990 },
        { id: 3, nombre: 'Nombre Hotel', descripcion: 'Descripción hotel', precio: 332488 },
        { id: 4, nombre: 'Nombre Hotel', descripcion: 'Descripción hotel', precio: 14315 },
    ];

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
                    <p class="card-text">${hotel.descripcion}</p>
                    <button 
                        class="btn btn-primary agregar-carrito" 
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

        return card;
    }
});