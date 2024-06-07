from django.shortcuts import render
from django.utils.translation import activate
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url

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


def index(request):
    return render(request, 'index.html')

def infoHoteles(request):
    return render(request, 'infoHoteles.html')
