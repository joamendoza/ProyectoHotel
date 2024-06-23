from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    nombre = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    puntos = models.IntegerField(default=0)
    historial_reservas = models.TextField(null=True, blank=True)
    comentarios_valoraciones = models.TextField(null=True, blank=True)
    roles = models.ManyToManyField('Role', related_name='usuarios', blank=True)
    foto_perfil = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"Usuario {self.id}: {self.email}"

class Role(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


