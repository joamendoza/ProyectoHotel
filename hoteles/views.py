from datetime import datetime
import json
import locale
import requests
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.utils.translation import activate, gettext as _
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.urls import reverse, translate_url
from .models import Hotel, Habitacion, Reserva, Valoracion
from usuarios.models import Usuario, TarjetaPuntos
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views import View
from .forms import FiltroHabitacionesForm, FiltroReservasForm, HabitacionForm, MultipleHabitacionForm, ValoracionForm
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q


def superuser_required(user):
    return user.is_superuser

# Create your views here.
def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language and language in dict(settings.LANGUAGES):
            activate(language)
            # Redirigir a la URL traducida
            next_url = request.META.get('HTTP_REFERER', '/')
            next_url_translated = translate_url(next_url, language)
            response = HttpResponseRedirect(next_url_translated)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return HttpResponseRedirect('/')

def get_hoteles(request):
    categoria = request.GET.get('categoria')
    en_oferta = request.GET.get('en_oferta')
    search_term = request.GET.get('search')

    # Construir el filtro dinámicamente
    filtros = {}
    if categoria:
        filtros['categoria'] = categoria
    if en_oferta:
        filtros['en_oferta'] = True

    # Filtrar por término de búsqueda
    if search_term:
        hoteles = Hotel.objects.filter(
            Q(nombre__icontains=search_term) |  # Buscar por nombre (ignorando mayúsculas y minúsculas)
            Q(descripcion_breve__icontains=search_term) |  # Buscar por descripción breve
            Q(descripcion_detallada__icontains=search_term) |  # Buscar por descripción detallada
            Q(categoria__icontains=search_term) |  # Buscar por categoría (ignorando mayúsculas y minúsculas)
            Q(ubicacion__icontains=search_term)  # Buscar por ubicación (ignorando mayúsculas y minúsculas)
        ).filter(**filtros) if filtros else Hotel.objects.filter(
            Q(nombre__icontains=search_term) |
            Q(descripcion_breve__icontains=search_term) |
            Q(descripcion_detallada__icontains=search_term) |
            Q(categoria__icontains=search_term) |
            Q(ubicacion__icontains=search_term)
        )
    else:
        hoteles = Hotel.objects.filter(**filtros) if filtros else Hotel.objects.all()

    data = [{
        'id': hotel.id,
        'nombre': hotel.nombre,
        'descripcion_breve': hotel.descripcion_breve,
        'descripcion_detallada': hotel.descripcion_detallada,
        'precio': hotel.precio,
        'precio_con_descuento': hotel.precio_con_descuento(),
        'foto': hotel.foto.url if hotel.foto else '',
        'en_oferta': hotel.en_oferta,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'categoria': hotel.categoria,
        'wifi_gratuito': hotel.wifi_gratuito,
        'desayuno_incluido': hotel.desayuno_incluido,
        'gimnasio': hotel.gimnasio,
        'piscina': hotel.piscina,
        'spa': hotel.spa,
        'restaurante': hotel.restaurante,
        'servicio_transporte': hotel.servicio_transporte,
        'servicios_eventos': hotel.servicios_eventos,
        'servicio_conserjeria': hotel.servicio_conserjeria,
        'ubicacion': hotel.ubicacion
    } for hotel in hoteles]

    return JsonResponse(data, safe=False)

def index(request):
    return render(request, 'index.html')

def infoHoteles(request):
    return render(request, 'infoHoteles.html')


def hotel_detalle_api(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel_data = {
        'id': hotel.id,
        'nombre': hotel.nombre,
        'descripcion_detallada': hotel.descripcion_detallada,
        'precio': hotel.precio,
        'foto': hotel.foto.url,
        'en_oferta': hotel.en_oferta,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'stock_habitaciones': hotel.stock_habitaciones
    }
    return JsonResponse(hotel_data)

def hotel_detalle_api(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    habitaciones = Habitacion.objects.filter(hotel=hotel, ocupada=False)
    habitaciones_data = [
        {
            'numero': habitacion.numero,
            'cantidad_camas': habitacion.cantidad_camas,
            'descripcion': habitacion.descripcion,
            'ocupada': habitacion.ocupada
        }
        for habitacion in habitaciones
    ]
    hotel_data = {
        'id': hotel.id,
        'nombre': hotel.nombre,
        'precio': hotel.precio,
        'descripcion_detallada': hotel.descripcion_detallada,
        'foto': hotel.foto.url,
        'habitaciones': habitaciones_data,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'ubicacion': hotel.ubicacion,
        'wifi': hotel.wifi_gratuito,
        'desayuno': hotel.desayuno_incluido,
        'gimnasio': hotel.gimnasio,
        'piscina': hotel.piscina,
        'spa': hotel.spa,
        'restaurante': hotel.restaurante,
        'transporte': hotel.servicio_transporte,
        'eventos': hotel.servicios_eventos,
        'conserjeria': hotel.servicio_conserjeria,
    }
    return JsonResponse(hotel_data)

def obtener_hoteles(request):
    hoteles = Hotel.objects.all()
    hoteles_data = []
    for hotel in hoteles:
        precio_con_descuento = hotel.precio_con_descuento() if hotel.en_oferta else hotel.precio
        hotel_data = {
            'id': hotel.id,
            'nombre': hotel.nombre,
            'descripcion_breve': hotel.descripcion_breve,
            'descripcion_detallada': hotel.descripcion_detallada,
            'precio': hotel.precio,
            'foto': hotel.foto.url,
            'categoria': hotel.categoria,
            'en_oferta': hotel.en_oferta,
            'porcentaje_descuento': hotel.porcentaje_descuento,
            'stock_habitaciones': hotel.stock_habitaciones,
            'precio_con_descuento': precio_con_descuento
        }
        hoteles_data.append(hotel_data)
    
    return JsonResponse(hoteles_data, safe=False)

@login_required
def infoHotelesID(request, hotel_id):
    try:
        usuario_actual = request.user
        hoteles_visitados_ids = usuario_actual.hoteles_vistos_ids.split(',') if usuario_actual.hoteles_vistos_ids else []
        if str(hotel_id) in hoteles_visitados_ids:
            hoteles_visitados_ids.remove(str(hotel_id))
        hoteles_visitados_ids.insert(0, str(hotel_id))
        usuario_actual.hoteles_vistos_ids = ','.join(hoteles_visitados_ids)
        usuario_actual.save()
        hotel_seleccionado = get_object_or_404(Hotel, id=hotel_id)
        context = {
            'hotel_seleccionado': hotel_seleccionado
        }
        return render(request, 'infoHoteles.html', context)
    except Hotel.DoesNotExist:
        return HttpResponse('Hotel no encontrado', status=404)
    
@login_required
def reservar_habitacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        hotel_id = data.get('hotel_id')
        habitacion_id = data.get('habitacion_id')

        hotel = get_object_or_404(Hotel, id=hotel_id)
        habitacion = get_object_or_404(Habitacion, numero=habitacion_id, hotel=hotel)

        if not habitacion.ocupada:
            habitacion.ocupada = True
            habitacion.save()
            Reserva.objects.create(
                usuario=request.user,
                hotel=hotel,
                habitacion=habitacion,
                fecha_ingreso=data.get('fecha_inicio'),
                fecha_salida=data.get('fecha_salida'),
            )
            return JsonResponse({'success': 'Reserva realizada con éxito'})
        else:
            return JsonResponse({'error': 'La habitación ya está ocupada'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@user_passes_test(superuser_required)
def crear_multiple_habitaciones(request):
    if request.method == 'POST':
        form = MultipleHabitacionForm(request.POST)
        if form.is_valid():
            hotel = form.cleaned_data['hotel']
            numero_pisos = form.cleaned_data['numero_pisos']
            habitaciones_por_piso = form.cleaned_data['habitaciones_por_piso']
            cantidad_camas = form.cleaned_data['cantidad_camas']
            
            for piso in range(1, numero_pisos + 1):
                for num in range(1, habitaciones_por_piso + 1):
                    numero = f'{piso}{num:02d}'
                    Habitacion.objects.create(
                        hotel=hotel,
                        numero=numero,
                        cantidad_camas=cantidad_camas,
                        descripcion='',
                        ocupada=False
                    )
            return redirect('lista_habitaciones')
    else:
        form = MultipleHabitacionForm()
    return render(request, './habitaciones/crear_multiple_habitaciones.html', {'form': form})

@user_passes_test(superuser_required)
def actualizar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, './habitaciones/actualizar_habitacion.html', {'form': form})

@user_passes_test(superuser_required)
def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('lista_habitaciones')
    return render(request, './habitaciones/eliminar_habitacion.html', {'habitacion': habitacion})

@user_passes_test(superuser_required)
def lista_habitaciones(request):
    form = FiltroHabitacionesForm(request.GET)
    habitaciones = Habitacion.objects.all()

    if form.is_valid():
        hotel = form.cleaned_data['hotel']
        ocupada = form.cleaned_data['ocupada']
        cantidad_camas = form.cleaned_data['cantidad_camas']

        if hotel:
            habitaciones = habitaciones.filter(hotel=hotel)
        if ocupada is not None:
            habitaciones = habitaciones.filter(ocupada=ocupada)
        if cantidad_camas:
            habitaciones = habitaciones.filter(cantidad_camas=cantidad_camas)

    paginator = Paginator(habitaciones, 10)  # Mostrar 10 habitaciones por página
    page_number = request.GET.get('page')
    habitaciones = paginator.get_page(page_number)

    return render(request, './habitaciones/lista_habitaciones.html', {
        'habitaciones': habitaciones,
        'form': form,
        'hoteles': Hotel.objects.all(),
    })

def reporte_reservas(request):
    form = FiltroReservasForm(request.GET)
    reservas = Reserva.objects.all()

    if form.is_valid():
        hotel = form.cleaned_data['hotel']
        habitacion = form.cleaned_data['habitacion']
        usuario = form.cleaned_data['usuario']
        fecha_salida = form.cleaned_data['fecha_salida']

        if hotel:
            reservas = reservas.filter(hotel=hotel)
        if habitacion:
            reservas = reservas.filter(habitacion=habitacion)
        if usuario:
            reservas = reservas.filter(usuario=usuario)
        if fecha_salida:
            reservas = reservas.filter(fecha_salida__date=fecha_salida)

    total_habitaciones = Habitacion.objects.count()
    habitaciones_ocupadas = Reserva.objects.filter(fecha_salida__isnull=True).count()
    porcentaje_ocupacion = (habitaciones_ocupadas / total_habitaciones) * 100 if total_habitaciones > 0 else 0

    context = {
        'reservas': reservas,
        'form': form,
        'hoteles': Hotel.objects.all(),
        'habitaciones': Habitacion.objects.all(),
        'total_habitaciones': total_habitaciones,
        'habitaciones_ocupadas': habitaciones_ocupadas,
        'porcentaje_ocupacion': porcentaje_ocupacion,
    }

    return render(request, './reportes/reporte_reservas.html', context)

@login_required
def perfilUsuario(request):
    usuario = request.user
    return render(request, 'perfilUsuario.html', {'usuario': usuario})

@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombreUsuario')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmar_contraseña = request.POST.get('confirmarContraseña')
        if password != confirmar_contraseña:
            return JsonResponse({'error': 'Las contraseñas no coinciden'})
        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El correo electrónico ya está registrado'})
        if Usuario.objects.filter(usuario=nombre_usuario).exists():
            return JsonResponse({'error': 'El nombre de usuario ya está registrado'})
        usuario = Usuario.objects.create(usuario=nombre_usuario, email=email)
        usuario.set_password(password)
        usuario.save()
        user = authenticate(request, username=nombre_usuario, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Usuario creado y logueado exitosamente'})
        else:
            return JsonResponse({'error': 'Error al autenticar al usuario'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('loginUsuario')
        password = request.POST.get('loginPassword')
        if not nombre_usuario or not password:
            return JsonResponse({'error': 'Por favor, ingresa un correo electrónico y una contraseña'}, status=400)
        user = authenticate(request, username=nombre_usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return JsonResponse({'error': 'Correo electrónico o contraseña incorrectos'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def actualizar_foto_perfil(request):
    if request.method == 'POST' and request.FILES['foto_perfil']:
        usuario = request.user
        usuario.foto_perfil = request.FILES['foto_perfil']
        usuario.save()
        return redirect('perfil')
    else:
        return JsonResponse({'error': 'No se pudo actualizar la foto de perfil'}, status=400)

@csrf_exempt
@login_required
def eliminar_cuenta(request):
    usuario = request.user
    logout(request)  # Cierra la sesión del usuario
    usuario.delete()  # Elimina el usuario de la base de datos
    messages.success(request, _("Tu cuenta ha sido eliminada con éxito."))
    return redirect('index')

@login_required
def valorar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.reserva = reserva
            valoracion.usuario = request.user
            valoracion.save()
            return JsonResponse({'message': 'Valoración guardada correctamente'})
    else:
        form = ValoracionForm()
    
    return render(request, 'valorar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def obtener_valoraciones_usuario(request):
    usuario_actual = request.user
    valoraciones_usuario = Valoracion.objects.filter(usuario=usuario_actual).values('reserva_id')

    valoraciones = list(valoraciones_usuario)  # Convertir a lista de diccionarios

    return JsonResponse({'valoraciones': valoraciones})

@login_required
def obtener_informacion_perfil(request):
    user = request.user
    data = {
        'username': user.usuario,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'email': user.email,
        'puntos': user.puntos,
        'lista_cupones': json.loads(user.lista_cupones) if user.lista_cupones else {},
        'hoteles_vistos': user.hoteles_vistos_ids,
    }
    return JsonResponse(data)

@login_required
def obtener_informacion_perfil_reservas(request):
    usuario = request.user
    reservas = Reserva.objects.filter(usuario=usuario)
    valoraciones = Valoracion.objects.filter(usuario=usuario)
    reservas_data = []
    for reserva in reservas:
        reservas_data.append({
            'id': reserva.id,
            'hotel_nombre': reserva.hotel.nombre,
            'hotel_descripcion_breve': reserva.hotel.descripcion_breve,
            'hotel_foto': reserva.hotel.foto.url,
            'fecha_reserva': reserva.fecha_reserva,
            'fecha_inicio': reserva.fecha_ingreso,
            'fecha_salida': reserva.fecha_salida,
            'valorar_url': reverse('valorar_reserva', args=[reserva.id]),
            'ver_reserva_url': reverse('ver_reserva', args=[reserva.id]),
            'checkout': reserva.checkout
        })
    valoraciones_data = list(valoraciones.values('reserva_id'))
    
    return JsonResponse({'reservas': reservas_data, 'valoraciones': valoraciones_data})

from django.utils import timezone

@login_required
def ver_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    ahora = timezone.now()
    fecha_ingreso = timezone.make_aware(reserva.fecha_ingreso) if timezone.is_naive(reserva.fecha_ingreso) else reserva.fecha_ingreso
    fecha_salida = timezone.make_aware(reserva.fecha_salida) if reserva.fecha_salida and timezone.is_naive(reserva.fecha_salida) else ahora
    dias_reserva = (fecha_salida - fecha_ingreso).days + 1

    precio_total = reserva.hotel.precio * dias_reserva
    if reserva.hotel.porcentaje_descuento:
        descuento = precio_total * (reserva.hotel.porcentaje_descuento / 100)
    else:
        descuento = 0
    precio_total_con_descuento = precio_total - descuento

    # Manejar el cupón seleccionado
    cupon_codigo = request.POST.get('cupon_codigo')
    cupon_descuento = 0
    if cupon_codigo:
        lista_cupones = json.loads(request.user.lista_cupones) if request.user.lista_cupones else {}
        cupon_info = lista_cupones.get(cupon_codigo)
        if cupon_info and cupon_info["count"] > 0:
            cupon_descuento = precio_total_con_descuento * (cupon_info["descuento"] / 100)
            # Actualizar la cantidad de cupones
            lista_cupones[cupon_codigo]["count"] -= 1
            request.user.lista_cupones = json.dumps(lista_cupones)
            request.user.save()

    precio_final = precio_total_con_descuento - cupon_descuento

    return render(request, 'ver_reserva.html', {
        'reserva': reserva,
        'precio_total': round(precio_total_con_descuento, 2),
        'precio_final': round(precio_final, 2),
        'cupon_descuento': round(cupon_descuento, 2),
        'cupones': [
            {
                "codigo": codigo,
                "descuento": detalles["descuento"],
                "count": detalles["count"],
            }
            for codigo, detalles in json.loads(request.user.lista_cupones).items()
        ] if request.user.lista_cupones else []
    })

def actualizar_descuento(request):
    if request.method == 'POST':
        usuario = request.user
        descuento = request.POST.get('descuento')
        if descuento is not None:
            usuario.descuento = descuento
            usuario.save()
            return JsonResponse({'status': 'success', 'descuento': descuento})
        return JsonResponse({'status': 'error', 'message': 'Descuento no proporcionado'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def desglose_precio(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    ahora = timezone.now()
    fecha_ingreso = timezone.make_aware(reserva.fecha_ingreso) if timezone.is_naive(reserva.fecha_ingreso) else reserva.fecha_ingreso
    fecha_salida = timezone.make_aware(reserva.fecha_salida) if reserva.fecha_salida and timezone.is_naive(reserva.fecha_salida) else ahora
    dias_reserva = (fecha_salida - fecha_ingreso).days + 1

    precio_por_noche = reserva.hotel.precio
    subtotal = precio_por_noche * dias_reserva
    descuento = reserva.usuario.descuento or 0
    total = subtotal * (1 - (descuento / 100))

    data = {
        'precio_por_noche': round(precio_por_noche, 2),
        'total_noches': dias_reserva,
        'subtotal': round(subtotal, 2),
        'descuento': descuento,
        'total': round(total, 2),
    }
    return JsonResponse(data)

@login_required
def enviar_valoracion_y_tarjeta(request):
    if request.method == 'POST':
        usuario = request.user
        form = ValoracionForm(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.usuario = usuario
            valoracion.save()

        # Buscar una tarjeta de puntos válida
        tarjeta = TarjetaPuntos.objects.filter(activa=True, canjeada_por__isnull=True).order_by('puntos').first()
        
        if tarjeta:
            tarjeta.canjear(usuario)
            tarjeta_codigo = tarjeta.codigo
            tarjeta_puntos = tarjeta.puntos
        else:
            tarjeta_codigo = None
            tarjeta_puntos = 0
        
        # Enviar correo de confirmación
        subject = 'Confirmación de Valoración y Tarjeta de Puntos'
        message = f'''
Estimado/a {usuario.usuario},

Hemos recibido su valoración. Gracias por su feedback.

Como agradecimiento, le hemos asignado una tarjeta de puntos con el código: {tarjeta_codigo} y valor de {tarjeta_puntos} puntos.

---

Saludos,
Equipo de Soporte
'''
        recipient_list = [usuario.email]
        send_mail(
            subject,
            message,
            'a.veranium@gmail.com',
            recipient_list,
            fail_silently=False,
        )
        
        return JsonResponse({'success': 'Valoración enviada y tarjeta de puntos asignada', 'tarjeta_codigo': tarjeta_codigo, 'tarjeta_puntos': tarjeta_puntos})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#ayuda correo
@login_required
def enviar_correo_ayuda(request):
    usuario = request.user
    subject = 'Solicitud de Asistencia'
    message = f'''
Estimado/a {usuario.usuario},

Hemos recibido su solicitud de asistencia. Favor de indicar detalladamente el problema que está experimentando, respondiendo este correo, para que podamos ayudarle de la mejor manera posible.

---

Saludos,
Equipo de Soporte
'''
    recipient_list = [usuario.email]
    send_mail(
        subject,
        message,
        'a.veranium@gmail.com',
        recipient_list,
        fail_silently=False,
    )
    return JsonResponse({'success': 'Correo de asistencia enviado con éxito', 'email': usuario.email})



#Cupones
@user_passes_test(superuser_required)
def crear_tarjetas(request):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 10))  # Valor por defecto: 10
        valor = int(request.POST.get('valor', 50))  # Valor por defecto: 50
        for _ in range(cantidad):
            codigo = get_random_string(length=12)
            TarjetaPuntos.objects.create(codigo=codigo, puntos=valor)

        messages.success(request, f'Se han creado {cantidad} tarjetas de puntos con valor {valor} correctamente.')
        return redirect('index')
    return render(request, 'crear_tarjetas.html')

@login_required
def canjear_puntos(request):
    if request.method == 'POST':
        puntos_requeridos = int(request.POST.get('puntos_requeridos'))
        descuento = int(request.POST.get('descuento'))
        usuario = request.user

        if usuario.puntos >= puntos_requeridos:
            usuario.puntos -= puntos_requeridos

            if usuario.lista_cupones:
                lista_cupones = json.loads(usuario.lista_cupones)
            else:
                lista_cupones = {}

            cupon_key = f"{puntos_requeridos}_{descuento}"
            if cupon_key in lista_cupones:
                lista_cupones[cupon_key]['count'] += 1
            else:
                lista_cupones[cupon_key] = {'count': 1, 'descuento': descuento}

            usuario.lista_cupones = json.dumps(lista_cupones)
            usuario.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No tienes suficientes puntos para realizar este canje.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)



class ValidarCodigoView(View):
    def post(self, request, *args, **kwargs):
        codigo = request.POST.get('codigo', '')
        try:
            tarjeta = TarjetaPuntos.objects.get(codigo=codigo, activa=True)
            return HttpResponse(status=200)  # Código válido
        except TarjetaPuntos.DoesNotExist:
            return HttpResponse(status=400)  # Código no válido

class AgregarPuntosView(View):
    def post(self, request, *args, **kwargs):
        codigo = request.POST.get('codigo', '')
        try:
            tarjeta = TarjetaPuntos.objects.get(codigo=codigo, activa=True)
            usuario = Usuario.objects.get(id=request.user.id)  # Obtener el usuario autenticado
            usuario.puntos += tarjeta.puntos
            usuario.save()
            tarjeta.activa = False
            tarjeta.save()
            tarjeta.canjeada_por = usuario
            tarjeta.save()
            return HttpResponse(status=200)  # Puntos agregados correctamente
        except TarjetaPuntos.DoesNotExist:
            return HttpResponse(status=400)  # Código no válido

#cambio de contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if not request.user.check_password(current_password):
            return JsonResponse({'error': 'La contraseña actual es incorrecta.'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'error': 'Las nuevas contraseñas no coinciden.'}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Mantiene al usuario logueado después del cambio de contraseña
        return JsonResponse({'success': '¡Tu contraseña ha sido cambiada exitosamente!'})

    return render(request, 'change_password.html')

#vista hoteles
def hoteles_api(request):
    categoria = request.GET.get('categoria')
    en_oferta = request.GET.get('en_oferta')

    print('holaaazaaaaaaaaaa')
    filtros = {}
    if categoria:
        filtros['categoria'] = categoria
    if en_oferta:
        filtros['en_oferta'] = en_oferta.lower() == 'true'

    hoteles = Hotel.objects.filter(**filtros)

    data = [{
        'id': hotel.id,
        'nombre': hotel.nombre,
        'descripcion_breve': hotel.descripcion_breve,
        'descripcion_detallada': hotel.descripcion_detallada,
        'precio': hotel.precio,
        'foto': hotel.foto.url,
        'en_oferta': hotel.en_oferta,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'categoria': hotel.categoria,
    } for hotel in hoteles]

    return JsonResponse(data, safe=False)

#API para obtener clima
def obtener_clima(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    api_key = 'a821304f76c0eb391f25f7727ee562b7'  # Reemplaza con tu API key de OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={hotel.ubicacion}&appid={api_key}&units=metric&lang=es"

    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        clima = {
            'temperatura': data['main']['temp'],
            'descripcion': data['weather'][0]['description'],
            'icono': data['weather'][0]['icon'],
        }
        return JsonResponse(clima)
    else:
        return JsonResponse({'error': 'No se pudo obtener el clima'}, status=500)
    

#Pago
def convertir_fecha(fecha_str):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Remover "de" para facilitar el parseo y capitalizar el mes
        fecha_str = fecha_str.replace(' de ', ' ').capitalize()

        # Parsear la fecha utilizando el nuevo formato
        fecha_datetime = datetime.strptime(fecha_str, "%d %B %Y %H:%M")
        
        # Formatear la fecha en el formato deseado YYYY-MM-DD HH:MM:SS
        fecha_formato = fecha_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        return fecha_formato
    
    except Exception as e:
        print(f"Error al convertir fecha: {e}")
        return None

def checkout_view(request):
    total_amount = request.GET.get('amount')
    hotel_name = request.GET.get('hotel')
    fecha_reserva = request.GET.get('fecha_reserva')
    fecha_ingreso = request.GET.get('fecha_ingreso')
    fecha_salida_raw = request.GET.get('fecha_salida')
    room_number = request.GET.get('room')
    cupon = request.GET.get('cupon')

    fecha_reserva = fecha_reserva.replace("Fecha de Reserva: ", "").strip()
    fecha_ingreso = fecha_ingreso.replace("Fecha de Ingreso: ", "").strip()
    room_number = room_number.replace("Habitación: ", "").strip()

    try:
        # Convertir fecha_salida_raw al formato deseado
        fecha_salida = convertir_fecha(fecha_salida_raw)

        if not fecha_salida:
            raise ValueError("No se pudo convertir la fecha de salida")
        user = request.user

        hotel = get_object_or_404(Hotel, nombre=hotel_name)
        habitacion = get_object_or_404(Habitacion, numero=room_number, hotel=hotel)

        reserva = get_object_or_404(Reserva, usuario=user, hotel=hotel, habitacion=habitacion)
        reserva.fecha_salida = fecha_salida
        reserva.save()
        reserva.checkout = True
        reserva.save()
        if cupon and user.lista_cupones:
            cupones = json.loads(user.lista_cupones)
            if cupon in cupones:
                cupones[cupon]['count'] -= 1
                if cupones[cupon]['count'] == 0:
                    del cupones[cupon]
                user.lista_cupones = json.dumps(cupones)
                user.save()
        return redirect(reverse('qr_code_url') + f'?amount={total_amount}&hotel={hotel_name}&fecha_reserva={fecha_reserva}&fecha_ingreso={fecha_ingreso}&fecha_salida={fecha_salida_raw}&room={room_number}')

    except Exception as e:
        print(f"Error en la vista checkout_view: {e}")
        return HttpResponseServerError("Ha ocurrido un error al procesar la solicitud. Por favor, inténtalo de nuevo más tarde.")
    
def qr_code_view(request):
    total_amount = request.GET.get('amount')
    hotel_name = request.GET.get('hotel')
    fecha_reserva = request.GET.get('fecha_reserva')
    fecha_ingreso = request.GET.get('fecha_ingreso')
    fecha_salida = request.GET.get('fecha_salida')
    room_number = request.GET.get('room')
    
    context = {
        'total_amount': total_amount,
        'hotel_name': hotel_name,
        'fecha_reserva': fecha_reserva,
        'fecha_ingreso': fecha_ingreso,
        'fecha_salida': fecha_salida,
        'room_number': room_number,
    }
    return render(request, 'qr_code_template.html', context)

