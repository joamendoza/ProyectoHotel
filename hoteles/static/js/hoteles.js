document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');
    const navLinks = document.querySelectorAll('.nav-link');

    function formatearPrecio(precio) {
        const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        });
        return formatter.format(precio);
    }

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
            window.location.href = `/informacion-hotel/${hotel.id}/`;
        });

        const nuevaCard = card.querySelector('.card');
        const imagen = nuevaCard.querySelector('.card-img-top');
        imagen.style.width = '400px';
        imagen.style.height = '600px';
        imagen.style.display = 'block';
        imagen.style.margin = '0 auto';

        const cuerpoTarjeta = nuevaCard.querySelector('.card-body');
        cuerpoTarjeta.style.display = 'flex';
        cuerpoTarjeta.style.flexDirection = 'column';
        cuerpoTarjeta.style.justifyContent = 'center';
        cuerpoTarjeta.style.height = '100%';

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

    fetch(`/api/hoteles/${hotelId}/`)
        .then(response => response.json())
        .then(hotelSeleccionado => {
            if (hotelSeleccionado) {
                hotelInfoContainer.innerHTML = `
                    <div class="card mb-3" style="width: 940px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${hotelSeleccionado.foto}" class="img-fluid rounded-start" alt="Imagen hotel">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${hotelSeleccionado.nombre}</h5>
                                    <p class="card-text">Precio por noche: ${new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(hotelSeleccionado.precio)}</p>
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
                    const isAuthenticated = true; // Reemplazar con la autenticación real
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
                                // Redireccionar a una página de confirmación o a la misma página del hotel
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
