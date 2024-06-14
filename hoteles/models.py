from django.db import models

# Create your models here.
class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion_breve = models.CharField(max_length=500)
    descripcion_detallada = models.TextField()
    precio = models.IntegerField()
    foto = models.ImageField(upload_to='hoteles/')

    def __str__(self):
         return f"Hotel {self.id}: {self.nombre}"

# Pequeña adición que corrige el plural de Django al generar la tabla
class Meta:
    verbose_name_plural = "Hoteles"