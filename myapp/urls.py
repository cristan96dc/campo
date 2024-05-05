from django.urls import path
from myapp import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views. signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('deportes/', views.lista_deportes, name='lista_deportes'), 
    path('perfil/', views.profile, name='perfil'),
    path('detalle_deporte/<int:deporte_id>/', views.detalle_deporte, name='detalle_deporte'),
    path('agregar-comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('deportes/<int:deporte_id>/anotarse/', views.anotarse, name='anotarse'),
    path('deportes/<int:deporte_id>/no_anotarse/', views.no_anotarse, name='no_anotarse'),
    path('perfil_ver/<str:username>/', views.ver_perfil_otro_usuario, name='ver_perfil_otro_usuario'),
    path('crear-foro/', views.crear_foro, name='crear_foro'),
    path('ver-foros/', views.ver_foros, name='ver_foros'),
    path('detalle-foro/<int:foro_id>/', views.detalle_foro, name='detalle_foro'),
    path('borrar_foro/<int:foro_id>/', views.borrar_foro, name='borrar_foro'),
    path('anotado/', views.anotado, name='anotado'),  # Cambio realizado
    path('contactos/', views.lista_de_contactos, name='contactos'),
    path('chat/<int:destinatario_id>/', views.chat, name='chat'),


    




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)