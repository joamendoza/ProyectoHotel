from django.db import models
from django.dispatch import receiver
from usuarios.models import Usuario
from django.db.models.signals import post_save

# Create your models here.
class Hotel(models.Model):
    CATEGORIAS = [
        ('normal', 'Normal'),
        ('frente_al_mar', 'Frente al Mar'),
        ('cabanas', 'Cabañas'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion_breve = models.CharField(max_length=500)
    descripcion_detallada = models.TextField()
    precio = models.IntegerField()
    foto = models.ImageField(upload_to='hoteles/')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='normal')
    en_oferta = models.BooleanField(default=False)
    porcentaje_descuento = models.IntegerField(default=0)
    stock_habitaciones = models.PositiveIntegerField(default=0)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)

    #Servicios adicionales:
    wifi_gratuito = models.BooleanField(default=False)
    desayuno_incluido = models.BooleanField(default=False)
    gimnasio = models.BooleanField(default=False)
    piscina = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    restaurante = models.BooleanField(default=False)
    servicio_transporte = models.BooleanField(default=False)
    servicios_eventos = models.BooleanField(default=False)
    servicio_conserjeria = models.BooleanField(default=False)

    @property
    def todas_las_habitaciones(self):
        return self.habitaciones.all()

    def __str__(self):
        return f"Hotel {self.id}: {self.nombre}"
    
    def precio_con_descuento(self):#por algun motivo siempre devuelve undefined, no se por que, pero meh
        if self.en_oferta and self.porcentaje_descuento > 0:
            descuento = self.precio * self.porcentaje_descuento / 100
            return int(self.precio - descuento)
        return self.precio

    
    def reservar_habitacion(self):
        if self.stock_habitaciones > 0:
            self.stock_habitaciones -= 1
            self.save()
            return True
        return False

# Pequeña adición que corrige el plural de Django al generar la tabla
class Meta:
    verbose_name_plural = "Hoteles"

class Habitacion(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='habitaciones', on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    cantidad_camas = models.PositiveIntegerField()
    descripcion = models.TextField()
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Habitación {self.numero} en {self.hotel.nombre}"



class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_ingreso = models.DateTimeField(null=True, blank=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva {self.id} de {self.usuario.usuario} en {self.hotel.nombre}"
    
class Valoracion(models.Model):
    valoracion_id = models.AutoField(primary_key=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()
    fecha_valoracion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Valoracion id {self.valoracion_id} de {self.usuario.usuario} en {self.reserva.hotel}"
    
@receiver(post_save, sender=Habitacion)
def add_habitacion_to_hotel(sender, instance, created, **kwargs):
    if created:
        hotel = instance.hotel
        hotel.habitaciones.add(instance)
        hotel.save()
