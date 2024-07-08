document.addEventListener('DOMContentLoaded', () => {
    const hotelesContainer = document.getElementById('hoteles-container');
    const navLinks = document.querySelectorAll('.nav-link');
    const searchInput = document.getElementById('busquedaHoteles');

    if (!hotelesContainer) {
        console.error('El contenedor de hoteles no existe en el DOM.');
        return;
    }
    
    function formatearPrecio(precio) {
        if (isNaN(precio)) return 'N/A';
        const formatter = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        });
        return formatter.format(precio);
    }

    function obtenerClima(ubicacion, callback) {
        const apiKey = 'a821304f76c0eb391f25f7727ee562b7'; // Reemplaza con tu API key de OpenWeatherMap
        const url = `http://api.openweathermap.org/data/2.5/weather?q=${ubicacion}&appid=${apiKey}&units=metric&lang=es`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.cod === 200) {
                    const clima = {
                        temperatura: Math.round(data.main.temp),
                        descripcion: data.weather[0].description,
                        icono: data.weather[0].icon,
                    };
                    callback(clima);
                } else {
                    callback(null);
                }
            })
            .catch(error => {
                console.error('Error al obtener el clima:', error);
                callback(null);
            });
    }

    function crearCardProducto(hotel) {
        const card = document.createElement('div');
        card.classList.add('col-md-3', 'mb-4');
        let precioDescuento = `<h4 class="card-title">${formatearPrecio(hotel.precio)}</h4>`;

        const badgesServicios = [];

        if (hotel.wifi_gratuito) {
            badgesServicios.push('<span class="badge bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill">Wi-Fi</span>');
        }
        if (hotel.desayuno_incluido) {
            badgesServicios.push('<span class="badge bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill">Desayuno</span>');
        }
        if (hotel.gimnasio) {
            badgesServicios.push('<span class="badge bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill">Gimnasio</span>');
        }
        if (hotel.piscina) {
            badgesServicios.push('<span class="badge bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill">Piscina</span>');
        }
        if (hotel.spa) {
            badgesServicios.push('<span class="badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis rounded-pill">Spa</span>');
        }
        if (hotel.restaurante){
            badgesServicios.push('<span class="badge bg-danger-subtle border border-danger-subtle text-danger-emphasis rounded-pill">Restaurante</span>');
        }
        if (hotel.servicio_transporte) {
            badgesServicios.push('<span class="badge bg-dark-subtle border border-dark-subtle text-dark-emphasis rounded-pill">Transporte</span>');
        }
        if (hotel.servicios_eventos) {
            badgesServicios.push('<span class="badge bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill">Eventos</span>');
        }
        if (hotel.servicio_conserjeria) {
            badgesServicios.push('<span class="badge bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill">Conserjería</span>');
        }

        if (hotel.porcentaje_descuento && hotel.porcentaje_descuento > 0) {
            precioDescuento = `
                <h4 class="card-title text-danger">${formatearPrecio(hotel.precio_con_descuento)}</h4>
                <p class="text-muted"><s>${formatearPrecio(hotel.precio)}</s></p>
                <span class="badge bg-danger">${hotel.porcentaje_descuento}% OFF</span>
            `;
        }

        card.innerHTML = `
            <div class="card" style="height: 100%;">
                <img src="${hotel.foto}" class="card-img-top" alt="Imagen Hotel" style="object-fit: cover; height: 300px;">
                <div class="card-body d-flex flex-column justify-content-between">
                    ${precioDescuento}
                    <p class="card-title">${hotel.nombre}</p>
                    <p class="card-text">${hotel.descripcion_breve}</p>
                    <div class="clima-info" data-ubicacion="${hotel.ubicacion}">Cargando clima...</div>
                    <div class="servicios-adicionales mb-1">
                        ${badgesServicios.join(' ')}
                    </div>
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

        // Obtener y mostrar el clima
        const climaInfo = card.querySelector('.clima-info');
        obtenerClima(hotel.ubicacion, (clima) => {
            if (clima) {
                climaInfo.innerHTML = `
                    <p><img src="http://openweathermap.org/img/wn/${clima.icono}.png" alt="Icono Clima">Temperatura: ${clima.temperatura}°C</p>
                `;
            } else {
                climaInfo.innerHTML = 'No se pudo obtener el clima';
            }
        });

        return card;
    }

    function obtenerHoteles(filtro = '') {
        let url = '/api/hoteles/';
        if (filtro) {
            url += `?${filtro}`;
            console.log('URL:', url);
        }

        fetch(url)
            .then(response => response.json())
            .then(hoteles => {
                console.log('URL:', url);
                console.log('Hoteles con filtro:', hoteles);
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
            console.log('Filtro:', filtro);
            let filtroQuery = '';

            switch (filtro) {
                case 'ofertas':
                    filtroQuery = 'en_oferta=true';
                    break;
                case 'todos':
                    filtroQuery = '';
                    break;
                case 'frente_al_mar':
                    filtroQuery = 'categoria=frente_al_mar';
                    break;
                case 'cabanas':
                    filtroQuery = 'categoria=cabanas';
                    break;
                default:
                    filtroQuery = '';
                    break;
            }

            obtenerHoteles(filtroQuery);
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.trim();
            obtenerHoteles(`search=${encodeURIComponent(searchTerm)}`);
        });

        searchInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                const searchTerm = searchInput.value.trim();
                obtenerHoteles(`search=${encodeURIComponent(searchTerm)}`);
            }
        });
    } else {
        console.error('El campo de búsqueda no existe en el DOM.');
    }

    obtenerHoteles();
});




document.addEventListener('DOMContentLoaded', () => {
    const hotelInfoContainer = document.getElementById('hotel-info');
    const hotelId = window.location.pathname.split('/')[2];
    localStorage.removeItem('hotelSeleccionado');

    function obtenerClima(ubicacion, callback) {
        const apiKey = 'a821304f76c0eb391f25f7727ee562b7'; // Reemplaza con tu API key de OpenWeatherMap
        const url = `http://api.openweathermap.org/data/2.5/weather?q=${ubicacion}&appid=${apiKey}&units=metric&lang=es`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.cod === 200) {
                    const clima = {
                        temperatura: Math.round(data.main.temp),
                        descripcion: data.weather[0].description,
                        icono: data.weather[0].icon,
                    };
                    callback(clima);
                } else {
                    console.error(`Error al obtener el clima: ${data.message}`);
                    callback(null);
                }
            })
            .catch(error => {
                console.error('Error al obtener el clima:', error);
                callback(null);
            });
    }

    fetch(`/api/hoteles/${hotelId}`)
        .then(response => response.json())
        .then(hotelSeleccionado => {
            if (hotelSeleccionado) {
                console.log('Datos del hotel seleccionado:', hotelSeleccionado);

                const { precioConDescuento, precioDescuentoHTML } = calcularPrecioConDescuento(hotelSeleccionado.precio, hotelSeleccionado.porcentaje_descuento);
                console.log('Precio con descuento:', precioConDescuento, 'Porcentaje descuento: ', hotelSeleccionado.porcentaje_descuento, 'HTML del precio:', precioDescuentoHTML);
                const badgesServicios = [];

                if (hotelSeleccionado.wifi) {
                    badgesServicios.push('<span class="badge bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill">Wi-Fi</span>');
                }
                if (hotelSeleccionado.desayuno) {
                    badgesServicios.push('<span class="badge bg-success-subtle border border-success-subtle text-success-emphasis rounded-pill">Desayuno</span>');
                }
                if (hotelSeleccionado.gimnasio) {
                    badgesServicios.push('<span class="badge bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill">Gimnasio</span>');
                }
                if (hotelSeleccionado.piscina) {
                    badgesServicios.push('<span class="badge bg-primary-subtle border border-primary-subtle text-primary-emphasis rounded-pill">Piscina</span>');
                }
                if (hotelSeleccionado.spa) {
                    badgesServicios.push('<span class="badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis rounded-pill">Spa</span>');
                }
                if (hotelSeleccionado.restaurante) {
                    badgesServicios.push('<span class="badge bg-danger-subtle border border-danger-subtle text-danger-emphasis rounded-pill">Restaurante</span>');
                }
                if (hotelSeleccionado.transporte) {
                    badgesServicios.push('<span class="badge bg-dark-subtle border border-dark-subtle text-dark-emphasis rounded-pill">Transporte</span>');
                }
                if (hotelSeleccionado.eventos) {
                    badgesServicios.push('<span class="badge bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill">Eventos</span>');
                }
                if (hotelSeleccionado.conserjeria) {
                    badgesServicios.push('<span class="badge bg-light-subtle border border-light-subtle text-light-emphasis rounded-pill">Conserjería</span>');
                }
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
                                    <div class="clima-info" data-ubicacion="${hotelSeleccionado.ubicacion}">Cargando clima...</div>
                                    <label for="habitacionesSelect">Selecciona una habitación:</label>
                                    <select id="habitacionesSelect">
                                        <!-- Aquí se llenarán las opciones con JavaScript -->
                                    </select>
                                    <br><br>
                                    <label for="fechaInicio">Ingreso:</label>
                                    <input type="date" id="fechaInicio" name="fechaInicio" min="${new Date().toISOString().split('T')[0]}">
                                    <br><br>
                                    <label for="fechaSalida">Salida (opcional):</label>
                                    <input type="date" id="fechaSalida" name="fechaSalida" disabled>
                                    <br><br>
                                    <div class="servicios-adicionales mt-3 mb-3">
                                         ${badgesServicios.join(' ')}
                                    </div>
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

                const fechaInicio = document.getElementById('fechaInicio');
                const fechaSalida = document.getElementById('fechaSalida');

                fechaInicio.addEventListener('change', () => {
                    fechaSalida.min = fechaInicio.value;
                    fechaSalida.disabled = false;
                });

                const reservarBtn = document.getElementById('reservarBtn');
                reservarBtn.addEventListener('click', () => {
                    const isAuthenticated = true; // Aquí puedes integrar tu lógica de autenticación
                    const habitacionSeleccionada = habitacionesSelect.value;
                    const fechaInicioValue = fechaInicio.value;
                    const fechaSalidaValue = fechaSalida.value;

                    if (!fechaInicioValue) {
                        alert('Debes seleccionar una fecha de inicio para la reserva.');
                        return;
                    }

                    const requestBody = {
                        hotel_id: hotelSeleccionado.id,
                        habitacion_id: habitacionSeleccionada,
                        fecha_inicio: fechaInicioValue
                    };

                    if (fechaSalidaValue) {
                        requestBody.fecha_salida = fechaSalidaValue;
                    }

                    if (isAuthenticated) {
                        fetch('/api/reservar/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(requestBody)
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

                // Obtener y mostrar el clima
                const climaInfo = document.querySelector('.clima-info');
                if (hotelSeleccionado.ubicacion) {
                    obtenerClima(hotelSeleccionado.ubicacion, (clima) => {
                        if (clima) {
                            climaInfo.innerHTML = `
                                <p>Temperatura: ${clima.temperatura}°C</p>
                                <p><img src="http://openweathermap.org/img/wn/${clima.icono}.png" alt="Icono Clima"> ${clima.descripcion}</p>
                            `;
                        } else {
                            climaInfo.innerHTML = 'No se pudo obtener el clima';
                        }
                    });
                } else {
                    climaInfo.innerHTML = 'Ubicación no disponible para obtener el clima';
                }

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
