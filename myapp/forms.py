from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Foro, ComentarioForo, Comentario
from django import forms
from .models import Mensaje


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

from django import forms
from .models import OtraClase

class OtraClaseForm(forms.ModelForm):
    class Meta:
        model = OtraClase
        fields = ['edad', 'foto_de_perfil', 'descripcion']
        
class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ['titulo', 'descripcion', 'deporte']
        from django import forms

class NuevoComentarioForm(forms.Form):
    contenido = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']
        widgets = {
            'destinatario': forms.Select(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }