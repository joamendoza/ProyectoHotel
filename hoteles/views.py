from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import translate_url
from .models import Hotel
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

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
    hoteles = list(Hotel.objects.values())
    return JsonResponse(hoteles, safe=False)

def index(request):
    return render(request, 'index.html')

def infoHoteles(request):
    return render(request, 'infoHoteles.html')

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

@csrf_exempt
@login_required
def eliminar_cuenta(request):
    usuario = request.user
    logout(request)  # Cierra la sesión del usuario
    usuario.delete()  # Elimina el usuario de la base de datos
    messages.success(request, _("Tu cuenta ha sido eliminada con éxito."))
    return redirect('index')

def hoteles_api(request):
    categoria = request.GET.get('categoria')
    en_oferta = request.GET.get('en_oferta')

    if categoria:
        hoteles = Hotel.objects.filter(categoria=categoria)
    elif en_oferta:
        hoteles = Hotel.objects.filter(en_oferta=True)
    else:
        hoteles = Hotel.objects.all()

    data = [{
        'id': hotel.id,
        'nombre': hotel.nombre,
        'descripcion_breve': hotel.descripcion_breve,
        'descripcion_detallada': hotel.descripcion_detallada,
        'precio': hotel.precio,
        'precio_con_descuento': hotel.precio_con_descuento(),
        'foto': hotel.foto.url,
        'en_oferta': hotel.en_oferta,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'categoria': hotel.categoria,
    } for hotel in hoteles]

    return JsonResponse(data, safe=False)