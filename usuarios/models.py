from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string

def user_directory_path(instance, filename):
    # Almacena la imagen en: MEDIA_ROOT/usuarios/<id_usuario>/<filename>
    return f'usuarios/{instance.id}/{filename}'

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(usuario=usuario, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(usuario, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    puntos = models.IntegerField(default=0)
    hoteles_vistos_ids = models.TextField('IDs de hoteles visitados', blank=True)
    roles = models.ManyToManyField('Role', related_name='usuarios', blank=True)
    foto_perfil = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    descuento = models.IntegerField(default=0)
    lista_cupones = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']

    def agregar_valoracion(self, valoracion):
        if self.comentarios_valoraciones:
            comentarios = self.comentarios_valoraciones.split('\n')
        else:
            comentarios = []

        comentario_nuevo = f"Puntuación: {valoracion['puntuacion']}, Comentario: {valoracion['comentario']}"
        comentarios.append(comentario_nuevo)

        self.comentarios_valoraciones = '\n'.join(comentarios)
        self.save()

    def __str__(self):
        return f"Usuario {self.id}: {self.email}"

class Role(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class TarjetaPuntos(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    puntos = models.IntegerField(default=0)
    canjeada_por = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generar_codigo_unico()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tarjeta de Puntos {self.codigo}"

    def canjear(self, usuario):
        if self.activa:
            if not self.canjeada_por:
                self.canjeada_por = usuario
                usuario.puntos += self.puntos
                usuario.save()
                self.activa = False
                self.save()
                return True
        return False
    
    def asignar(self, usuario):
        if self.activa and not self.canjeada_por:
            self.canjeada_por = usuario
            self.save()
            return True
        return False

    def generar_codigo_unico(self):
        codigo_generado = get_random_string(length=12)
        while TarjetaPuntos.objects.filter(codigo=codigo_generado).exists():
            codigo_generado = get_random_string(length=12)
        return codigo_generado
