from rest_framework import serializers

from main.models import *


class MarcaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marca
        fields = ['url', 'id', 'nombre']


class VehiculoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['url', 'chasis', 'modelo', 'matricula', 'color', 'fecha_fabricacion', 'fecha_matriculacion',
                  'fecha_baja', 'suspendido', 'tipo_vehiculo', 'marca']


# Ejercicio 2

class PatineteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patinete
        fields = ['numero', 'url', 'tipo', 'precio_desbloqueo', 'precio_minuto']


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Usuario
        fields = ['url', 'debit', 'usuario']


class AlquilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alquiler
        fields = ['id', 'url', 'usuario', 'patinete', 'fecha_desbloqueo', 'fecha_entrega', 'coste_final']
