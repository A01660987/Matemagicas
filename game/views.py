from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterUserForm
from.models import *

def inicio(request):
    return render(request, 'inicio.html')

def login_user(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                messages.error(request,'inicia sesión como admin')
                return redirect('admin')
            else:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request,'usuario o contraseña incorrectos')
            return redirect('login')
    return render(request, 'login.html')

def login_admin(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('manage')
            else:
                messages.error(request,'inicia sesión como usuario')
                return redirect('login')
        else:
            messages.error(request,'usuario o contraseña incorrectos')
            return redirect('admin')
    return render(request, 'admin.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    return render(request, 'manage.html')

def register_user(request):
    if(request.method == 'POST'):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            profesor = Profesor(first_name=form.cleaned_data["first_name"],
                                last_name=form.cleaned_data["last_name"],
                                username=form.cleaned_data["username"],
                                password=form.cleaned_data["password1"])
            profesor.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, 'profesor registrado exitosamente')
            else:
                messages.error(request, 'error al registrar profesor')
        else:
            messages.error(request, 'error al registrar profesor')
    return redirect('manage')

def logout_user(request):
    logout(request)
    return redirect('login')

def validar_estudiante(request):
    if(request.method == 'POST'):
        grupo = request.POST['grupo']
        num_lista = request.POST['num_lista']
        try:
            alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
            nivel_actual = alumno.nivel_actual
            return JsonResponse({'nivel_actual': nivel_actual})
        except Alumno.DoesNotExist:
            return JsonResponse({'nivel_actual': 0})
        
def progreso(request):
    if(request.method == 'POST'):
        grupo = request.POST['grupo']
        num_lista = request.POST['num_lista']
        nivel_actual = request.POST['nivel_actual']
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        alumno.nivel_actual = nivel_actual
        alumno.save()
        pass
