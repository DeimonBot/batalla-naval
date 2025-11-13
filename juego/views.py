from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def inicio(request):
    return render(request, 'juego/inicio.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user:
            login(request, user)
            return redirect('inicio')
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