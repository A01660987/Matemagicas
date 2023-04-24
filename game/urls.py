from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login', views.login_user, name='login'),
    path('admin', views.login_admin, name='admin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/<int:numero>', views.dashboard_group, name='dashboard_group'),
    path('manage', views.manage, name='manage'),
    path('manage/<int:numero>', views.manage_group, name='manage_group'),
    path('new_alumno', views.new_alumno, name='new_alumno'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('newgroup', views.new_group, name='newgroup'),
    path('del_profe', views.del_profe, name='del_profe'),
    path('del_group', views.del_group, name='del_group'),
    path('del_alumno', views.del_alumno, name='del_alumno'),
    path('validar_estudiante', views.validar_estudiante, name='validar_estudiante'),
    path('progreso', views.progreso, name='progreso'),
    path('nuevo_intento', views.nuevo_intento, name='nuevo_intento'),
    path('obtener_aciertos', views.obtener_aciertos, name='obtener_aciertos'),
    path('promedio_grupo', views.promedio_grupo, name='promedio_grupo')
]