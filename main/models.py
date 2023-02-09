from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#Ejercicio 1
class Colores(models.TextChoices):
    AZUL = 'azul', 'Azul'
    AMARILLO = 'amarillo', 'Amarillo'
    ROJO = 'rojo', 'Rojo'
    VERDE = 'verde', 'VERDE'


class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre)


class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICE = [
        ('coche', 'Coche'),
        ('ciclomotor', 'Ciclomotor'),
        ('motocicleta', 'Motocicleta')
    ]
    chasis = models.IntegerField(primary_key=True, unique=True)
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=7, unique=True)
    color = models.CharField(max_length=50, choices=Colores.choices)
    fecha_fabricacion = models.DateField()
    fecha_matriculacion = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    suspendido = models.BooleanField(default=False)
    tipo_vehiculo = models.CharField(choices=TIPO_VEHICULO_CHOICE, max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.RESTRICT)

    def __str__(self):
        return '{} {} {} {} - Suspendido:{}'.format(self.chasis,self.modelo, self.color,self.tipo_vehiculo,self.suspendido)


# Ejercicio 2

class Patinete(models.Model):
    numero = models.IntegerField(primary_key=True, unique=True)
    tipo = models.CharField(max_length=50)
    precio_desbloqueo = models.DecimalField(max_digits=6, decimal_places=2)
    precio_minuto = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '{}: {} - {} - {}'.format(self.numero, self.tipo, self.precio_desbloqueo, self.precio_minuto)


class Usuario(models.Model):
    debit = models.FloatField(default=0)
    usuario = models.ForeignKey(User, to_field='username', unique=True,on_delete=models.RESTRICT)

    def __str__(self):
        return '{} - {}'.format(self.usuario, self.debit)


class Alquiler(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    patinete = models.ForeignKey(Patinete, on_delete=models.RESTRICT)
    fecha_desbloqueo = models.DateTimeField(null=True)
    fecha_entrega = models.DateTimeField(null=True)
    coste_final = models.FloatField(null=True)

    def __str__(self):
        return '{}: {} {} {} - Coste final:{}'.format(self.usuario, self.patinete, self.fecha_desbloqueo,
                                                      self.fecha_entrega,
                                                      self.coste_final)