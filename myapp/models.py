from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    nombre_completo = models.CharField(max_length=150)
    edad = models.PositiveIntegerField(null=True, blank=True)
    foto_de_perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    descripcion = models.TextField(blank=True)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    def __str__(self):
        return self.use
    
class Deporte(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    usuarios_que_dieron_like = models.ManyToManyField(User, related_name='likes_comentario', blank=True)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')

    def __str__(self):
        return self.contenido[:50]
    
class OtraClase(models.Model):
    edad = models.PositiveIntegerField(null=True, blank=True)
    foto_de_perfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    descripcion = models.TextField(blank=True)
    original = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"OtraClase de {self.original.username}"
    
    
class Foro(models.Model):
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    usuarios_que_dieron_like = models.ManyToManyField(User, related_name='likes_foro', blank=True)

    def __str__(self):
        return self.titulo

class ComentarioForo(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    foro = models.ForeignKey(Foro, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    usuarios_que_dieron_like = models.ManyToManyField(User, related_name='likes_comentario_foro', blank=True)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')

    def __str__(self):
        return self.contenido[:50]
    
    
class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'deporte']

    def __str__(self):
        return f"{self.usuario.username} - {self.deporte.nombre}"
    
    
class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.remitente} a {self.destinatario}'

    class Meta:
        ordering = ['-fecha_envio']