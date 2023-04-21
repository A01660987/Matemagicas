from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
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

def logout_user(request):
    logout(request)
    return redirect('inicio')

@login_required
def dashboard(request):
    profesor = Profesor.objects.get(username=request.user.username)
    grupos = Grupo.objects.filter(profesor=profesor)
    return render(request, 'dashboard.html', {'grupos': grupos})

@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    profesores = Profesor.objects.all()
    return render(request, 'manage.html', {'profesores': profesores})

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

def new_group(request):
    if(request.method == 'POST'):
        username = request.POST['profesor']
        numero = request.POST['numero']
        try:
            grupo = Grupo.objects.get(numero=numero)
            messages.error(request, 'un grupo con ese número ya existe')
        except Grupo.DoesNotExist:
            profesor = Profesor.objects.get(username=username)
            grupo = Grupo(profesor=profesor, numero=numero)
            grupo.save()
            messages.success(request, 'grupo creado exitosamente')
    return redirect('manage')

@csrf_exempt
def validar_estudiante(request):
    if(request.method == 'POST'):
        grupo = request.POST.get('grupo')
        num_lista = request.POST.get('num_lista')
        try:
            alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
            return JsonResponse({'nivel_actual': alumno.nivel_actual})
        except Alumno.DoesNotExist:
            return JsonResponse({'nivel_actual': 0})

@csrf_exempt        
def progreso(request):
    if(request.method == 'POST'):
        grupo = request.POST['grupo']
        num_lista = request.POST['num_lista']
        nivel_actual = request.POST['nivel_actual']
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        alumno.nivel_actual = nivel_actual
        alumno.save()
        pass