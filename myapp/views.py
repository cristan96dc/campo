from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Deporte, Comentario, CustomUser, OtraClase, Foro ,ComentarioForo, Inscripcion, Mensaje
from .forms import CustomUserCreationForm, ForoForm, ComentarioForm, NuevoComentarioForm
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import OtraClaseForm
from django.contrib.auth.models import User
from .forms import MensajeForm
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.





def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'saludo': True})
    else:
        return render(request, 'home.html', {'login_button': True})
    

def lista_deportes(request):
    deportes = Deporte.objects.all()
    tipos_deporte = Deporte.objects.values_list('tipo', flat=True).distinct()
    tipo_seleccionado = request.GET.get('tipo')
    
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        saludo = True
        login_button = False
    else:
        saludo = False
        login_button = True

    if tipo_seleccionado:
        deportes = deportes.filter(tipo=tipo_seleccionado)

    return render(request, 'lista_deportes.html', {'deportes': deportes, 'tipos_deporte': tipos_deporte, 'tipo_seleccionado': tipo_seleccionado, 'saludo': saludo, 'login_button': login_button})
    

def detalle_deporte(request, deporte_id):
    deporte = get_object_or_404(Deporte, pk=deporte_id)
    if request.user.is_authenticated:
        saludo = True
        login_button = False
    else:
        saludo = False
        login_button = True
    return render(request, 'detalle_deporte.html', {'deporte': deporte, 'saludo': saludo, 'login_button': login_button})


@login_required
def anotarse(request, deporte_id):
    deporte = get_object_or_404(Deporte, pk=deporte_id)

    # Verificar si el usuario ya está inscrito en el deporte
    usuario_inscrito = Inscripcion.objects.filter(usuario=request.user, deporte=deporte).exists()
    
    # Si ya está inscrito, redirigir a otra página
    if usuario_inscrito:
        return redirect('anotado')  # Reemplaza 'otra_pagina' con el nombre de tu URL
    
    # Si no está inscrito, crear una nueva inscripción
    Inscripcion.objects.create(usuario=request.user, deporte=deporte)

    return render(request, 'anotarse.html', {'deporte': deporte, 'usuario_inscrito': usuario_inscrito})

def no_anotarse(request, deporte_id):

    return redirect('detalle_deporte', deporte_id=deporte_id)

@login_required
def anotado(request):
    # Aquí podrías realizar cualquier otra lógica relacionada con la anotación si lo necesitas
    # Si no necesitas usar el deporte_id, puedes eliminar la línea siguiente
    # deporte = get_object_or_404(Deporte, pk=deporte_id)
   return render(request, 'anotado.html') 



@login_required
def profile(request):
    user = request.user
    otra_clase = OtraClase.objects.filter(original=user).first()

    if not otra_clase:
        otra_clase = OtraClase(original=user)
        otra_clase.save()

    foros_creados = Foro.objects.filter(creador=user)

    # Obtener las inscripciones de deportes del usuario
    inscripciones_usuario = Inscripcion.objects.filter(usuario=user)

    if request.method == 'POST':
        form = OtraClaseForm(request.POST, request.FILES, instance=otra_clase)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = OtraClaseForm(instance=otra_clase)

    foto_de_perfil_url = otra_clase.foto_de_perfil.url if otra_clase and otra_clase.foto_de_perfil else None

    # Verificar si el usuario está autenticado para mostrar el botón de inicio de sesión
    saludo = request.user.is_authenticated  

    return render(request, 'perfil.html', {
        'user': user,
        'otra_clase': otra_clase,
        'form': form,
        'foto_de_perfil_url': foto_de_perfil_url,
        'foros_creados': foros_creados,
        'inscripciones_usuario': inscripciones_usuario,
        'saludo': saludo  # Pasar el valor de autenticación a la plantilla
    })
    
 
@login_required   
def borrar_foro(request, foro_id):
    if request.method == 'POST':
        # Verificar si el foro pertenece al usuario actual antes de eliminarlo
        foro = Foro.objects.get(id=foro_id)
        if foro.creador == request.user:
            foro.delete()
    return redirect('perfil')

@login_required
def agregar_comentario(request):
    return render(request, "hola")


#mejorar esta parte y no tine el nav
@login_required
def ver_perfil_otro_usuario(request, username):
    # Obtener el usuario del perfil
    otro_usuario = get_object_or_404(User, username=username)
    
    # Obtener la instancia de OtraClase asociada al usuario del perfil
    otra_clase = OtraClase.objects.filter(original=otro_usuario).first()
    
    # Obtener la URL de la foto de perfil si existe
    foto_de_perfil_url = otra_clase.foto_de_perfil.url if otra_clase and otra_clase.foto_de_perfil else None

    # Obtener los foros creados por el usuario del perfil
    foros_creados = Foro.objects.filter(creador=otro_usuario)
    
    saludo = request.user.is_authenticated      
    return render(request, 'ver_perfil_otro_usuario.html', {
        'user': otro_usuario,
        'otra_clase': otra_clase,
        'foto_de_perfil_url': foto_de_perfil_url,
        'foros_creados': foros_creados,
        'mostrar_botones': False, 
        'saludo': saludo , 
        })
    
    
@login_required
def crear_foro(request):
    if request.method == 'POST':
        form = ForoForm(request.POST)
        if form.is_valid():
            foro = form.save(commit=False)
            foro.creador = request.user
            foro.save()
            return redirect('ver_foros')
    else:
        form = ForoForm()
    
    # Verificar si el usuario está autenticado para mostrar el botón de inicio de sesión
    saludo = request.user.is_authenticated  
    
    return render(request, 'crear_foro.html', {'form': form, 'saludo': saludo})


def ver_foros(request):
    lista_foros = Foro.objects.all()
    
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        saludo = True
        login_button = False
    else:
        saludo = False
        login_button = True

    return render(request, 'ver_foros.html', {'lista_foros': lista_foros, 'saludo': saludo,'saludo': saludo, 'login_button': login_button})






def detalle_foro(request, foro_id):
    foro = get_object_or_404(Foro, pk=foro_id)
    comentarios = foro.comentarios.all()  # Obtener todos los comentarios relacionados con este foro

    if request.method == 'POST':
        if 'like_button_foro' in request.POST:
            if request.user.is_authenticated:
                # Verificar si el usuario ya dio like al foro
                if request.user in foro.usuarios_que_dieron_like.all():
                    foro.likes -= 1
                    foro.usuarios_que_dieron_like.remove(request.user)
                else:
                    foro.likes += 1
                    foro.usuarios_que_dieron_like.add(request.user)
                foro.save()
                return redirect('detalle_foro', foro_id=foro_id)
            else:
                # Manejar el caso si el usuario no está autenticado
                return redirect('login')  # Redirigirlo a la página de inicio de sesión
        elif 'like_button' in request.POST:
            if request.user.is_authenticated:
                comentario_id = request.POST.get('comentario_id')  # Obtener el ID del comentario
                comentario = get_object_or_404(ComentarioForo, pk=comentario_id)

                # Verificar si el usuario ya dio like al comentario
                if request.user in comentario.usuarios_que_dieron_like.all():
                    comentario.likes -= 1
                    comentario.usuarios_que_dieron_like.remove(request.user)
                else:
                    comentario.likes += 1
                    comentario.usuarios_que_dieron_like.add(request.user)
                comentario.save()
                return redirect('detalle_foro', foro_id=foro_id)
            else:
                # Manejar el caso si el usuario no está autenticado
                return redirect('login')  # Redirigirlo a la página de inicio de sesión
        else:
            form = NuevoComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario = form.cleaned_data['contenido']
                ComentarioForo.objects.create(
                    autor=request.user,
                    foro=foro,
                    contenido=nuevo_comentario
                )
                return redirect('detalle_foro', foro_id=foro_id)
    else:
        form = NuevoComentarioForm()

    # Verificar si el usuario está autenticado para mostrar el botón de inicio de sesión
    if request.user.is_authenticated:
        saludo = True
        login_button = False
    else:
        saludo = False
        login_button = True 

    return render(request, 'detalle_foro.html', {'foro': foro, 'comentarios': comentarios, 'form': form, 'saludo': saludo, 'login_button': login_button })


@login_required
def lista_de_contactos(request):
    q = request.GET.get('q')
    # Obtener los mensajes más recientes enviados y recibidos por el usuario
    mensajes_enviados = Mensaje.objects.filter(remitente=request.user).order_by('-fecha_envio').select_related('destinatario').first()
    mensajes_recibidos = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio').select_related('remitente').first()

    # Inicializar un diccionario para almacenar la fecha del último mensaje para cada contacto
    last_message_dates = {}

    # Actualizar el diccionario con la fecha del último mensaje para cada destinatario de los mensajes enviados
    if mensajes_enviados:
        last_message_dates[mensajes_enviados.destinatario] = mensajes_enviados.fecha_envio

    # Actualizar el diccionario con la fecha del último mensaje para cada remitente de los mensajes recibidos
    if mensajes_recibidos:
        last_message_dates[mensajes_recibidos.remitente] = mensajes_recibidos.fecha_envio

    # Crear una lista de contactos ordenados por la fecha del último mensaje
    contactos = sorted(last_message_dates.keys(), key=lambda contacto: last_message_dates[contacto], reverse=True)

    if q:
        # Filtrar los contactos por el nombre de usuario
        contactos = User.objects.filter(username__icontains=q)

    # Obtener la imagen de perfil de cada usuario, si está disponible
    for contacto in contactos:
        otra_clase = OtraClase.objects.filter(original=contacto).first()
        contacto.foto_de_perfil = otra_clase.foto_de_perfil if otra_clase else None

    return render(request, 'lista_contactos.html', {'contactos': contactos, 'saludo': True})



@login_required
def chat(request, destinatario_id):
    destinatario = User.objects.get(pk=destinatario_id)

    if request.method == 'POST':
        contenido = request.POST.get('message', '')
        if contenido:
            mensaje = Mensaje(remitente=request.user, destinatario=destinatario, contenido=contenido, fecha_envio=timezone.now())
            mensaje.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            else:
                return redirect('chat', destinatario_id=destinatario_id)
        else:
            return HttpResponseBadRequest("El contenido del mensaje no puede estar vacío.")

    mensajes = Mensaje.objects.filter(
        (Q(remitente=request.user) & Q(destinatario=destinatario)) |
        (Q(remitente=destinatario) & Q(destinatario=request.user))
    ).order_by('fecha_envio')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [{'remitente': mensaje.remitente.username, 'contenido': mensaje.contenido, 'fecha_envio': mensaje.fecha_envio.strftime('%Y-%m-%d %H:%M:%S')} for mensaje in mensajes]
        return JsonResponse(data, safe=False)

    return render(request, 'chat.html', {'destinatario': destinatario, 'mensajes': mensajes})

