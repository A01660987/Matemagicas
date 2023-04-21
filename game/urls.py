from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login', views.login_user, name='login'),
    path('admin', views.login_admin, name='admin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('manage', views.manage, name='manage'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('validar_estudiante', views.validar_estudiante, name='validar_estudiante'),
    path('progreso', views.progreso, name='progreso')
]