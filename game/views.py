from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterUserForm
from.models import *
import json

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

def dashboard_group(request, numero):
    profesor = Profesor.objects.get(username=request.user.username)
    grupo = Grupo.objects.get(numero=numero, profesor=profesor)
    alumnos = Alumno.objects.filter(grupo=grupo)
    promedio1 = promedio_grupo(numero, 1)
    promedio2 = promedio_grupo(numero, 2)
    promedio3 = promedio_grupo(numero, 3)
    eq1 = eq_grupo(numero, 1)
    eq2 = eq_grupo(numero, 2)
    eq3 = eq_grupo(numero, 3)
    eq4 = eq_grupo(numero, 4)
    eq5 = eq_grupo(numero, 5)
    return render(request, 'dashboard_group.html', {'grupo': grupo, 'alumnos': alumnos, 'promedio1': promedio1, 'promedio2': promedio2, 'promedio3': promedio3, 'eq1': eq1, 'eq2': eq2, 'eq3': eq3, 'eq4': eq4, 'eq5': eq5})

def dashboard_alumno(request, numero, lista):
    profesor = Profesor.objects.get(username=request.user.username)
    grupo = Grupo.objects.get(numero=numero, profesor=profesor)
    alumno = Alumno.objects.get(grupo=grupo, num_lista=lista)
    promedio1 = promedio_alumno(numero, lista, 1)
    promedio2 = promedio_alumno(numero, lista, 2)
    promedio3 = promedio_alumno(numero, lista, 3)
    eq1 = eq_alumno(numero, lista, 1)
    eq2 = eq_alumno(numero, lista, 2)
    eq3 = eq_alumno(numero, lista, 3)
    eq4 = eq_alumno(numero, lista, 4)
    eq5 = eq_alumno(numero, lista, 5)
    return render(request, 'dashboard_alumno.html', {'grupo': grupo, 'alumno': alumno, 'promedio1': promedio1, 'promedio2': promedio2, 'promedio3': promedio3, 'eq1': eq1, 'eq2': eq2, 'eq3': eq3, 'eq4': eq4, 'eq5': eq5})

@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    profesores = Profesor.objects.all()
    grupos = Grupo.objects.all()
    return render(request, 'manage.html', {'profesores': profesores, 'grupos': grupos})

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

def manage_group(request, numero):
    grupo = Grupo.objects.get(numero=numero)
    alumnos = Alumno.objects.filter(grupo=grupo)
    profesor = grupo.profesor
    return render(request, 'manage_group.html', {'grupo': grupo, 'alumnos': alumnos, 'profesor': profesor})

def new_alumno(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        numero = request.POST['numero']
        grupo = Grupo.objects.get(numero=numero)
        alumnos = Alumno.objects.filter(grupo=grupo)
        num_lista = 1
        for alumno in alumnos:
            if alumno.num_lista >= num_lista:
                num_lista = alumno.num_lista + 1
        try:
            alumno = Alumno(first_name=first_name, last_name=last_name, grupo=grupo, num_lista=num_lista, nivel_actual=1)
            alumno.save()
            messages.success(request, 'alumno creado exitosamente')
        except:
            messages.error(request, 'error al crear alumno')
        return redirect('manage_group', numero=numero)
    
def del_profe(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        profesor = Profesor.objects.get(username=username)
        user = User.objects.get(username=username)
        profesor.delete()
        user.delete()
        messages.success(request, 'profesor eliminado exitosamente')
    return redirect('manage')

def del_group(request):
    if (request.method == 'POST'):
        numero = request.POST['numero']
        grupo = Grupo.objects.get(numero=numero)
        grupo.delete()
        messages.success(request, 'grupo eliminado exitosamente')
    return redirect('manage')

def del_alumno(request):
    if (request.method == 'POST'):
        numero = request.POST['numero']
        grupo = Grupo.objects.get(numero=numero)
        num_lista = request.POST['num_lista']
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        alumno.delete()
        messages.success(request, 'alumno eliminado exitosamente')
    return redirect('manage_group', numero=numero)

@csrf_exempt
def validar_estudiante(request):
    if(request.method == 'POST'):
        numero = request.POST['grupo']
        num_lista = request.POST['num_lista']
        try:
            grupo = Grupo.objects.get(numero=numero)
            alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
            return JsonResponse({'nivel_actual': alumno.nivel_actual})
        except:
            return JsonResponse({'nivel_actual': 0})

@csrf_exempt        
def progreso(request):
    if(request.method == 'POST'):
        numero = request.POST['grupo']
        num_lista = request.POST['num_lista']
        nivel_actual = request.POST['nivel_actual']
        grupo = Grupo.objects.get(numero=numero)
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        alumno.nivel_actual = nivel_actual
        alumno.save()
        return JsonResponse({"success": True})

@csrf_exempt
def nuevo_intento(request):
    if(request.method == 'POST'):
        numero = request.POST['grupo']
        num_lista = request.POST['num_lista']
        aciertos = request.POST['aciertos']
        nivel = request.POST['nivel']
        grupo = Grupo.objects.get(numero=numero)
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        intento = Intentos(alumno=alumno, aciertos=aciertos, nivel=nivel)
        intento.save()
        return JsonResponse({"success": True})

def intentos_grupo(request, numero, nivel):
    grupo = Grupo.objects.get(numero=numero)
    alumnos = Alumno.objects.filter(grupo=grupo)
    intentos = Intentos.objects.filter(alumno__in=alumnos, nivel=nivel)
    datos = []
    for intento in intentos:
        datos.append({
            "aciertos": intento.aciertos,
            "timestamp": intento.timestamp
        })
    return JsonResponse({"intentos": datos})

def intentos_alumno(request, numero, lista, nivel):
    grupo = Grupo.objects.get(numero=numero)
    alumno = Alumno.objects.get(grupo=grupo, num_lista=lista)
    intentos = Intentos.objects.filter(alumno=alumno, nivel=nivel)
    datos = []
    for intento in intentos:
        datos.append({
            "aciertos": intento.aciertos,
            "timestamp": intento.timestamp
        })
    return JsonResponse({"intentos": datos})

def promedio_grupo(numero, nivel):
    suma = 0
    elementos = 0
    grupo = Grupo.objects.get(numero=numero)
    alumnos = Alumno.objects.filter(grupo=grupo)
    intentos = Intentos.objects.filter(alumno__in=alumnos, nivel=nivel)
    for intento in intentos:
        suma += intento.aciertos
        elementos += 1
    try:
        promedio = round(suma / elementos, 3)
    except:
        promedio = 0
    return promedio

def promedio_alumno(numero, lista, nivel):
    suma = 0
    elementos = 0
    grupo = Grupo.objects.get(numero=numero)
    alumno = Alumno.objects.get(grupo=grupo, num_lista=lista)
    intentos = Intentos.objects.filter(alumno=alumno, nivel=nivel)
    for intento in intentos:
        suma += intento.aciertos
        elementos += 1
    try:
        promedio = round(suma / elementos, 3)
    except:
        promedio = 0
    return promedio
    
def update(request):
    if(request.method == 'POST'):
        profesor = request.POST['profesor']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password1']
        user = User.objects.get(username=profesor)
        profe = Profesor.objects.get(username=profesor)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.save()
        profe.first_name = first_name
        profe.last_name = last_name
        profe.username = username
        profe.password = password
        profe.save()
        messages.success(request, 'profesor editado exitosamente')
    return redirect('manage')

@csrf_exempt
def equivocacion(request):
    if(request.method == 'POST'):
        numero = request.POST['grupo']
        num_lista = request.POST['num_lista']
        tipo = request.POST['tipo']
        grupo = Grupo.objects.get(numero=numero)
        alumno = Alumno.objects.get(grupo=grupo, num_lista=num_lista)
        equivocacion = Equivocaciones(alumno=alumno, tipo=tipo)
        equivocacion.save()
        return JsonResponse({"success": True})
    
def eq_grupo(numero, tipo):
    grupo = Grupo.objects.get(numero=numero)
    alumnos = Alumno.objects.filter(grupo=grupo)
    equivocaciones = Equivocaciones.objects.filter(alumno__in=alumnos, tipo=tipo)
    return len(equivocaciones)

def eq_alumno(numero, lista, tipo):
    grupo = Grupo.objects.get(numero=numero)
    alumno = Alumno.objects.get(grupo=grupo, num_lista=lista)
    equivocaciones = Equivocaciones.objects.filter(alumno=alumno, tipo=tipo)
    return len(equivocaciones)