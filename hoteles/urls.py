from django.contrib import admin
from django.urls import path
from hoteles.vista import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('informacion-hotel/', infoHoteles)
]
