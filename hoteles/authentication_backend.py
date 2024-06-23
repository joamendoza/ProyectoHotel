from django.contrib.auth.backends import BaseBackend
from .models import Usuario
from django.contrib.auth.hashers import check_password

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Usuario.objects.get(usuario=username)
            if check_password(password, user.password):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
