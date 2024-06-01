from django.contrib import admin
from django.urls import path
from hoteles.vista import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index)
]
