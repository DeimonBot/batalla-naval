from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear-sala/', views.crear_sala, name='crear_sala'),
    path('unirse-sala/', views.unirse_sala, name='unirse_sala'),
    path('logout/', views.logout_view, name='logout'),
]