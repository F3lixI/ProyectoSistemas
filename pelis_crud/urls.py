from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro', views.registrar, name='registrar'),
    path('login', views.iniciar_sesion, name='login' ),
    path('buscar', views.buscar_pelicula, name='buscar'),
    path('logout', views.cerrar_sesion, name='logout'),
]
