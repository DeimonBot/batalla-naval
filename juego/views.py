from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Sala, Partida, Barco
from django.shortcuts import get_object_or_404
from django.db import models
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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

@login_required
def crear_sala(request):
    if request.method == 'POST':
        sala = Sala.objects.create(jugador_1=request.user)
        return redirect('dashboard')  # o redirigir a la vista de la sala si la creas
    return HttpResponse("Método no permitido")

@login_required
def unirse_sala(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_sala')
        try:
            sala = Sala.objects.get(codigo=codigo, activa=True)
            if sala.jugador_2 is None and sala.jugador_1 != request.user:
                sala.jugador_2 = request.user
                sala.save()

                # Crear partida automáticamente
                partida = Partida.objects.create(
                    sala=sala,
                    jugador_1=sala.jugador_1,
                    jugador_2=sala.jugador_2,
                    turno_actual=sala.jugador_1  # o aleatorio si prefieres
                )

                return redirect('ver_partida', partida.codigo)
            else:
                return HttpResponse("Sala no disponible o ya completa.")
        except Sala.DoesNotExist:
            return HttpResponse("Código de sala inválido.")
    return HttpResponse("Método no permitido")

@login_required
def dashboard(request):
    jugador = request.user

    partidas_jugadas = Partida.objects.filter(models.Q(jugador_1=jugador) | models.Q(jugador_2=jugador)).count()
    victorias = Partida.objects.filter(ganador=jugador).count()
    partidas_activas = Partida.objects.filter(
        activa=True,
        turno_actual=jugador
    )

    salas_activas = Sala.objects.filter(
        activa=True
    ).filter(models.Q(jugador_1=jugador) | models.Q(jugador_2=jugador))

    contexto = {
        'jugador': jugador,
        'partidas': partidas_jugadas,
        'victorias': victorias,
        'partidas_activas': partidas_activas,
        'salas_activas': salas_activas,
    }
    return render(request, 'juego/dashboard.html', contexto)

@login_required
def ver_sala(request, codigo):
    sala = get_object_or_404(Sala, codigo=codigo)
    jugador = request.user
    es_jugador = jugador == sala.jugador_1 or jugador == sala.jugador_2

    if not es_jugador:
        return HttpResponse("No tienes acceso a esta sala.")

    return render(request, 'juego/sala.html', {'sala': sala, 'jugador': jugador})

@login_required
def ver_partida(request, codigo):
    partida = get_object_or_404(Partida, codigo=codigo)
    jugador = request.user
    if jugador != partida.jugador_1 and jugador != partida.jugador_2:
        return HttpResponse("No tienes acceso a esta partida.")
    return render(request, 'juego/partida.html', {'partida': partida, 'jugador': jugador})

def logout_view(request):
    logout(request)
    return redirect('inicio')  # Asegúrate de tener esta URL definida

@require_POST
@login_required
def guardar_barco(request, codigo):
    partida = get_object_or_404(Partida, codigo=codigo)
    jugador = request.user

    # Obtener datos del formulario o JSON
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST

    coordenadas = json.loads(data.get('coordenadas'))
    tamaño = int(data.get('tamaño'))

    # Validar tamaño
    if len(coordenadas) != tamaño:
        return JsonResponse({'error': 'Cantidad de coordenadas no coincide con el tamaño del barco'}, status=400)

    # Validar solapamiento
    barcos_existentes = Barco.objects.filter(partida=partida, jugador=jugador)
    coordenadas_existentes = set()
    for barco in barcos_existentes:
        coordenadas_existentes.update(barco.coordenadas)

    if any(coord in coordenadas_existentes for coord in coordenadas):
        return JsonResponse({'error': 'Las coordenadas se solapan con otro barco'}, status=400)

    # Guardar barco
    Barco.objects.create(
        partida=partida,
        jugador=jugador,
        tamaño=tamaño,
        coordenadas=coordenadas
    )

    return JsonResponse({'status': 'ok'})
