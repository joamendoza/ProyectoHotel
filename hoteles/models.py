from django.db import models
from usuarios.models import Usuario

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

    def __str__(self):
        return f"Hotel {self.id}: {self.nombre}"
    
    def precio_con_descuento(self):
        if self.en_oferta and self.porcentaje_descuento > 0:
            return self.precio * (1 - self.porcentaje_descuento / 100)
        return self.precio

# Pequeña adición que corrige el plural de Django al generar la tabla
class Meta:
    verbose_name_plural = "Hoteles"
