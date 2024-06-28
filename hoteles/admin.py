from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Valoracion)