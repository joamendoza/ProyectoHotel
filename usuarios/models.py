# usuarios/models.py
from django.db import models

def user_directory_path(instance, filename):
    # Almacena la imagen en: MEDIA_ROOT/usuarios/<id_usuario>/<filename>
    return f'usuarios/{instance.id}/{filename}'

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    puntos = models.IntegerField(default=0)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    preferencia_contacto = models.CharField(max_length=50, null=True, blank=True)
    idioma_preferido = models.CharField(max_length=50, null=True, blank=True)
    recibir_notificaciones = models.BooleanField(default=True)
    historial_reservas = models.TextField(null=True, blank=True)
    preferencias_habitaciones = models.TextField(null=True, blank=True)
    notas_especiales = models.TextField(null=True, blank=True)
    ultima_fecha_acceso = models.DateTimeField(null=True, blank=True)
    estado_cuenta = models.CharField(max_length=20, default='activo')
    preferencias_viaje = models.TextField(null=True, blank=True)
    comentarios_valoraciones = models.TextField(null=True, blank=True)
    consentimiento_marketing = models.BooleanField(default=True)
    logs_actividad = models.TextField(null=True, blank=True)
    roles = models.ManyToManyField('Role', related_name='usuarios', blank=True)
    foto_perfil = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return f"Usuario {self.id}: {self.email}"

class Role(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
