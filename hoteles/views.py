from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.http import JsonResponse
from .models import Hotel
from usuarios.models import Usuario

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

def perfilUsuario(request):
    return render(request, 'perfilUsuario.html')

# hoteles/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from usuarios.models import Usuario  # Asegúrate de importar el modelo correcto

def registrarUsuario(request):
    if request.method == 'POST':
        try:
            nombreUsuario = request.POST['nombreUsuario']
            email = request.POST['email']
            password = request.POST['password']
        except MultiValueDictKeyError:
            return HttpResponse("Todos los campos son requeridos.", status=400)

        usuario = Usuario.objects.create(usuario=nombreUsuario, email=email, password=password)
        return redirect('/')
    else:
        return render(request, 'index')  # Ajusta el nombre de la plantilla si es necesario
