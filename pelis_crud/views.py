from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Pelicula
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'home.html', {'peliculas': peliculas})

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Iniciar sesión
            user = form.get_user()
            login(request, user)
            # Redirigir a la página deseada después del inicio de sesión
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def buscar_pelicula(request):
    query = request.GET.get("q")
    
    peliculas = []
    
    if query:
        peliculas=Pelicula.objects.filter(
            Q(director__icontains=query)|
            Q(titulo__icontains=query)
        ).distinct()
        
    
    return render(request, 'search.html', {'peliculas': peliculas})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')