document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');
    const navLinks = document.querySelectorAll('.nav-link');

    function formatearPrecio(precio) {
        const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        });
        console.log(precio);
        console.log(formatter.format(precio));
        return formatter.format(precio);
    }

    function crearCardProducto(hotel) {
        const card = document.createElement('div');
        card.classList.add('col-md-3', 'mb-4');
        let precioDescuento = `<h4 class="card-title">${formatearPrecio(hotel.precio)}</h4>`;
        console.log(hotel.porcentaje_descuento);
        console.log(hotel.precio);
        if (hotel.porcentaje_descuento > 0) {
            console.log('entro');
            precio_con_descuento = hotel.precio * ((100 - hotel.porcentaje_descuento) / 100);
            precioDescuento = `
                <h4 class="card-title text-danger">${formatearPrecio(precio_con_descuento)}</h4>
                <p class="text-muted"><s>${formatearPrecio(hotel.precio)}</s></p>
                <span class="badge bg-danger">${hotel.porcentaje_descuento}% OFF</span>
            `;
        }
    
        card.innerHTML = `
            <div class="card" style="height: 100%;">
                <img src="/media/${hotel.foto}" class="card-img-top" alt="Imagen Hotel" style="object-fit: cover; height: 300px;">
                <div class="card-body d-flex flex-column justify-content-between">
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
            window.location.href = `/informacion-hotel/${hotel.id}/`;
        });
    
        return card;
    }
    
    

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

    obtenerHoteles();
});

document.addEventListener('DOMContentLoaded', () => {
    const hotelInfoContainer = document.getElementById('hotel-info');
    const hotelId = window.location.pathname.split('/')[2];
    localStorage.removeItem('hotelSeleccionado');
    
    fetch(`/api/hoteles/${hotelId}`)
        .then(response => response.json())
        .then(hotelSeleccionado => {
            if (hotelSeleccionado) {
                console.log('Datos del hotel seleccionado:', hotelSeleccionado);

                const { precioConDescuento, precioDescuentoHTML } = calcularPrecioConDescuento(hotelSeleccionado.precio, hotelSeleccionado.porcentaje_descuento);
                console.log('Precio con descuento:', precioConDescuento, 'Porcentaje descuento: ', hotelSeleccionado.porcentaje_descuento, 'HTML del precio:', precioDescuentoHTML);

                hotelInfoContainer.innerHTML = `
                    <div class="card mb-3" style="width: 940px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${hotelSeleccionado.foto}" class="img-fluid rounded-start" alt="Imagen hotel">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${hotelSeleccionado.nombre}</h5>
                                    <p class="card-text">Precio por noche: ${precioDescuentoHTML}</p>
                                    <br>
                                    <p class="card-text">${hotelSeleccionado.descripcion_detallada}</p>
                                    <label for="habitacionesSelect">Selecciona una habitación:</label>
                                    <select id="habitacionesSelect">
                                        <!-- Aquí se llenarán las opciones con JavaScript -->
                                    </select>
                                    <br><br>
                                    <button id="reservarBtn" class="btn btn-primary">Reservar ahora</button>
                                </div>   
                            </div>
                        </div>
                    </div>
                `;

                // Llenar opciones del select con las habitaciones disponibles
                const habitacionesOptions = hotelSeleccionado.habitaciones
                    .filter(habitacion => !habitacion.ocupada)
                    .map(habitacion => `<option value="${habitacion.numero}">Habitación ${habitacion.numero}</option>`);
                
                const habitacionesSelect = document.getElementById('habitacionesSelect');
                habitacionesSelect.innerHTML = habitacionesOptions.join('');

                const reservarBtn = document.getElementById('reservarBtn');
                reservarBtn.addEventListener('click', () => {
                    const isAuthenticated = true;
                    const habitacionSeleccionada = habitacionesSelect.value;

                    if (isAuthenticated) {
                        fetch('/api/reservar/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                hotel_id: hotelSeleccionado.id,
                                habitacion_id: habitacionSeleccionada
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Reserva realizada con éxito');
                                window.location.href = `/index/`;
                            } else {
                                alert(data.error || 'Hubo un error al procesar la reserva.');
                            }
                        })
                        .catch(error => {
                            console.error('Error al procesar la reserva:', error);
                            alert('Hubo un error al procesar la reserva.');
                        });
                    } else {
                        alert('Debes iniciar sesión para realizar una reserva.');
                        window.location.href = '/accounts/login/';
                    }
                });

                console.log(hotelSeleccionado);
            } else {
                hotelInfoContainer.innerHTML = '<p>No se encontró información del hotel seleccionado.</p>';
            }
        })
    .catch(error => console.error('Error al obtener la información del hotel:', error));
});

function formatearPrecio(precio) {
    const formatter = new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    });
    return formatter.format(precio);
}

function calcularPrecioConDescuento(precioBase, porcentajeDescuento) {
    let precioDescuentoHTML = `<h4 class="card-title">${formatearPrecio(precioBase)}</h4>`;
    let precioConDescuento = precioBase;

    if (porcentajeDescuento > 0) {
        precioConDescuento = precioBase * ((100 - porcentajeDescuento) / 100);
        precioDescuentoHTML = `
            <h4 class="card-title text-danger">${formatearPrecio(precioConDescuento)}</h4>
            <p class="text-muted"><s>${formatearPrecio(precioBase)}</s></p>
            <span class="badge bg-danger">${porcentajeDescuento}% OFF</span>
        `;
    }

    return {
        precioConDescuento: precioConDescuento,
        precioDescuentoHTML: precioDescuentoHTML
    };
}
