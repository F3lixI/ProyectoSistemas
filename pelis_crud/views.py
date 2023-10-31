from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Pelicula, Comentario, Usuario
from django.contrib.auth.decorators import login_required
from .forms import ComentarioForm, PeliculaForm



@login_required(login_url='/login')
def home(request):
    """Muestra la pagina principal del listado de peliculas
    Lista las primeras 8 peliculas"""
    peliculas = Pelicula.objects.order_by('?')[:8]
    return render(request, 'home.html', {'peliculas': peliculas})

def registrar(request):
    """Registra un usuario nuevo en la base de datos.
    En caso de ser una peticion GET, lleva al usuario al formulario de registro"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crea una instancia de Usuario relacionada con el nuevo usuario
            usuario = Usuario(usuario=user)
            usuario.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    """Realiza un logi usando la fucion de login de django, agregando una cookie de 
    sesion para la gestion de la misma.
    En caso de ser una peticion GET, lleva al usuario al formulario de login"""
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
    """Busca una pelicula que contenga el texto includio en el parametro 'q'
    """
    query = request.GET.get("q")
    
    peliculas = []
    
    if query:
        peliculas=Pelicula.objects.filter(
            Q(director__icontains=query)|
            Q(titulo__icontains=query)
        ).distinct()
        
    
    return render(request, 'search.html', {'peliculas': peliculas})

def cerrar_sesion(request):
    """Cierra la sesion activa, y borra la cookie de sesion por medio de la funcion incluida en django"""
    logout(request)
    return redirect('home')

#vista indivual de pelicula
@login_required(login_url='/login')
def pelicula(request, id):
    """Muestra los detalles de una pelicula, asi como los comentarios que los usuarios hayan dejado de esta"""
    comentarios = Comentario.objects.filter(pelicula=id)

    pelicula = Pelicula.objects.get(pk=id)
    return render(request, 'pelicula.html', {'pelicula': pelicula, 'comentarios': comentarios})

@login_required(login_url='/login')
def comentar(request, id):
    """Crea un nuevo comentario que posee el id de la pelicula que comentó el usuario. En caso de ser una request GET,
    lleva al usuario a la pelicula del id que se quiso comentar"""
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        if texto:
            pelicula = Pelicula.objects.get(pk=id)
            comentario = Comentario(usuario=request.user.usuario, pelicula=pelicula, texto=texto)
            comentario.save()
            return redirect('pelicula', id=id)
    else:
        return redirect('pelicula', id=id)
    
@login_required(login_url='/login')
def eliminar_comentario(request, id):
    """Elimina el comentario seleccionado, borrandolo de la base de datos"""
    comentario = Comentario.objects.get(pk=id)
    
    if request.user.usuario == comentario.usuario:
        comentario.delete()
        
    return redirect('pelicula', id=comentario.pelicula.id)

@login_required(login_url='/login')
def editar_comentario(request, id):
    """Edita un comentario elegido por el usuario.
    En caso de ser una peticion GET, lleva al usuario al formulario de edicion del comentario"""
    comentario = get_object_or_404(Comentario, pk=id)


    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('pelicula', id=comentario.pelicula.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'partials/editar_comentario.html', {'form': form, 'comentario': comentario})

@login_required(login_url='/login')
def agregar_pelicula(request):
    """Crea una pelicula con todos los datos necesarios.
    En caso de ser una peticion GET, lleva al usuario al formulario de creacion de pelicula"""
    if request.method == 'POST':
        # Procesar el formulario si se ha enviado
        form = PeliculaForm(request.POST)  # Usar un formulario para agregar películas
        if form.is_valid():
            form.instance.usuario = request.user.usuario
            form.save()
            return redirect('home')  # Redirigir a la página de inicio u otra vista
    else:
        # Mostrar el formulario en caso contrario
        form = PeliculaForm()  # Usar un formulario para agregar películas

    return render(request, 'agregar_pelicula.html', {'form': form})
    
@login_required(login_url='/login')
def eliminar_pelicula(request, id):
    """Elimina una pelicula"""
    pelicula = get_object_or_404(Pelicula, pk=id)
    
    if request.user.usuario == pelicula.usuario:
        pelicula.delete()
        
    return redirect('home')

def ver_perfil(request):
    """Lista los detalles de un perfil de un usuario, con todos sus comentarios y peliculas"""
    usuario = request.user.usuario
    peliculas = Pelicula.objects.filter(usuario=usuario)
    comentarios = Comentario.objects.filter(usuario=usuario)
    
    return render(request, 'perfil.html', {'usuario': usuario, 'peliculas': peliculas, 'comentarios': comentarios})