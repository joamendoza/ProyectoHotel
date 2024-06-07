from django.contrib import admin
from django.urls import path
from hoteles.vista import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),
    path('', index, name='index'),
    path('index/', index),
    path('informacion-hotel/', infoHoteles),
]