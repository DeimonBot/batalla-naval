from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


def inicio(request):
    return render(request, 'juego/inicio.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'juego/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'juego/login.html')

def registro_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        User.objects.create_user(username=usuario, password=clave)
        return redirect('login')
    return render(request, 'juego/registro.html')

@login_required
def dashboard(request):
    jugador = request.user
    # Aquí luego conectaremos con modelos de Partida
    contexto = {
        'jugador': jugador,
        'partidas': 0,
        'victorias': 0,
    }
    return render(request, 'juego/dashboard.html', contexto)

def crear_sala(request):
    return HttpResponse("Aquí se creará una sala de juego.")

def unirse_sala(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_sala')
        # Aquí luego validaremos si la sala existe
        return HttpResponse(f"Intentando unirse a la sala con código: {codigo}")
    return HttpResponse("Método no permitido")

def logout_view(request):
    logout(request)
    return redirect('inicio')  # Asegúrate de tener esta URL definida
