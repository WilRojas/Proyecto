from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.


# class Task(models.Model):
#     tittle = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     datecompleted = models.DateTimeField(null=True, blank=True)
#     important = models.BooleanField(default=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.tittle + ' - by ' + self.user.username


# class AuthUser(models.Model):
#     id = models.AutoField(primary_key=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField(default=False)
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField(default=False)
#     is_active = models.IntegerField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     user_type = models.CharField(max_length=30)

#     class Meta:
#         managed = False
#         db_table = 'auth_user'

#     def guardar(self, *args, **kwargs):
#         if self.pk is None:
#             self.set_password(self.password)

#         super().save(*args, **kwargs)


# usuarios
class UsuarioManager(BaseUserManager):

    def create_user(self, email, username, nombres, apellidos, tipo_usuario, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos,
            tipo_usuario=tipo_usuario
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, nombres, apellidos, tipo_usuario, password):

        user = self.create_user(
            email=email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            tipo_usuario=tipo_usuario,
            password=password
        )

        user.usuario_administrador = True
        user.save()
        return user


class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre Usuario', unique=True, max_length=100)
    email = models.EmailField('Correo Electronico', max_length=300, unique=True)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    tipo_usuario = models.CharField('Tipo Usuario', max_length=20)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'tipo_usuario']

    def __str__(self):
        return f'{self.nombres},{self.apeliidos}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
