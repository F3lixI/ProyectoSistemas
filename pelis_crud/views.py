from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.db.models import Q
from .models import Pelicula

# Create your views here.
def home(request):
    return render(request, 'home.html')

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

def buscar_pelicula(request):
    query = request.GET.get("q")
    
    pelicula = Pelicula.objects.all()
    
    if query:
        pelicula=Pelicula.objects.filter(
            Q(director__icontains=query)|
            Q(titulo__icontains=query)
        ).distinct()
        
    
    return render(request, 'search.html', {'pelicula': pelicula})
    