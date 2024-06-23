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
    return render(request, 'perfilUsuario.html')

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

        # Autenticar al usuario
        user = authenticate(request, username=nombre_usuario, password=password)
        if user is not None:
            # Iniciar sesión del usuario
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



