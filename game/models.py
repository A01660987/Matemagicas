from django.db import models

class Profesor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    
class Grupo(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    numero = models.IntegerField(unique=True)
    
class Alumno(models.Model):
    grupo = models.ForeignKey(Grupo, null=False, on_delete=models.CASCADE)
    num_lista = models.IntegerField(null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nivel_actual = models.IntegerField(default=1)
    
class Intentos(models.Model):
    alumno = models.ForeignKey(Alumno, null=False, on_delete=models.CASCADE)
    aciertos = models.IntegerField(null=False)
    nivel = models.IntegerField(null=False)
    timestamp = models.DateTimeField(auto_now=True)

class Equivocaciones(models.Model):
    alumno = models.ForeignKey(Alumno, null=False, on_delete=models.CASCADE)
    tipo = models.IntegerField(null=False)
