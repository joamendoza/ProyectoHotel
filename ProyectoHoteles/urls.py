"""ProyectoHoteles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hoteles.views import *
from hoteles import views
from usuarios import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),
    path('', index, name='index'),
    path('api/hoteles/', views.get_hoteles, name='get_hoteles'),
    path('index/', index),
    path('informacion-hotels/', infoHoteles),
    path('informacion-hotel/<int:hotel_id>/', infoHotelesID, name='info_hoteles'),
    path('api/hoteles/<int:hotel_id>/', hotel_detalle_api, name='hotel_detalle_api'),
    path('obtener-hoteles/', obtener_hoteles, name='obtener_hoteles'),
    path('api/reservar/', reservar_habitacion, name='reservar_hotel'),

    path('habitaciones/', lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/crear/', crear_multiple_habitaciones, name='crear_multiple_habitaciones'),
    path('habitaciones/actualizar/<int:pk>/', actualizar_habitacion, name='actualizar_habitacion'),
    path('habitaciones/eliminar/<int:pk>/', eliminar_habitacion, name='eliminar_habitacion'),

    path('reporte-reservas/', reporte_reservas, name='reporte_reservas'),

    path('perfil/',perfilUsuario, name='perfil'),
    path('registrarUsuario/', registrar_usuario, name='registrar_usuario'),
    path('actualizar-foto-perfil/', actualizar_foto_perfil, name='actualizar_foto_perfil'),
    path('valorar/<int:reserva_id>/', valorar_reserva, name='valorar_reserva'),
    path('obtener_valoraciones_usuario/', obtener_valoraciones_usuario, name='obtener_valoraciones_usuario'),
    path('obtener_informacion_perfil_reservas/', obtener_informacion_perfil_reservas, name='obtener_informacion_perfil_reservas'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('eliminar_cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('api/hoteles/', views.hoteles_api, name='hoteles_api'),
    path('obtener-informacion-perfil/', obtener_informacion_perfil, name='obtener_informacion_perfil'),
    path('obtener_informacion_perfil_reservas', obtener_informacion_perfil_reservas, name='obtener_informacion_perfil_reservas'),
    path('canjear-puntos/', canjear_puntos, name='canjear_puntos'),
    path('crear_tarjetas/', crear_tarjetas, name='crear_tarjetas'), # Crear Tarjetas de cupones 
    path('enviar_valoracion_y_tarjeta/', enviar_valoracion_y_tarjeta, name='enviar_valoracion_y_tarjeta'), 
    path('validar_codigo/', ValidarCodigoView.as_view(), name='validar_codigo'),
    path('agregar_puntos/', AgregarPuntosView.as_view(), name='agregar_puntos'),
    path('cambiar-contraseña/', change_password, name='change_password'),
    path('enviar_correo_ayuda/', enviar_correo_ayuda, name='enviar_correo_ayuda'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)