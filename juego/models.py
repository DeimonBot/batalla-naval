import random, string
from django.db import models
from django.contrib.auth.models import User

def generar_codigo():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + numeros

class Partida(models.Model):
    codigo = models.CharField(max_length=6, unique=True, default=generar_codigo)
    sala = models.OneToOneField('Sala', on_delete=models.CASCADE)
    jugador_1 = models.ForeignKey(User, related_name='partidas_jugador1', on_delete=models.CASCADE)
    jugador_2 = models.ForeignKey(User, related_name='partidas_jugador2', on_delete=models.CASCADE)
    turno_actual = models.ForeignKey(User, related_name='turno_actual', on_delete=models.SET_NULL, null=True, blank=True)
    ganador = models.ForeignKey(User, related_name='partidas_ganadas', on_delete=models.SET_NULL, null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partida {self.codigo}"

class Sala(models.Model):
    codigo = models.CharField(max_length=6, unique=True, default=generar_codigo)
    jugador_1 = models.ForeignKey(User, related_name='salas_creadas', on_delete=models.CASCADE)
    jugador_2 = models.ForeignKey(User, related_name='salas_unidas', on_delete=models.SET_NULL, null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sala {self.codigo}"
    
class Barco(models.Model):
    partida = models.ForeignKey('Partida', on_delete=models.CASCADE)
    jugador = models.ForeignKey(User, on_delete=models.CASCADE)
    tamaño = models.IntegerField()
    coordenadas = models.JSONField(default=list)  # Ej: [["A1", "A2", "A3"]]
    hundido = models.BooleanField(default=False)

    def __str__(self):
        return f"Barco de {self.tamaño} casillas ({self.jugador.username})"