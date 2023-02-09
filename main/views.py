from django.db import transaction
from django.db.models import Q, Count
from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from main.permissions import EsEditor
from main.serializer import *


# Create your views here.

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE' or self.request.method == 'PUT':
            self.permission_classes = [EsEditor]
        return super(MarcaViewSet, self).get_permissions()


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['fecha_fabricacion']
    filterset_fields = ['marca', 'color', 'modelo']

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE' or self.request.method == 'PUT':
            self.permission_classes = [EsEditor]
        return super(VehiculoViewSet, self).get_permissions()


# Ejercicio 2
class PatineteviewSet(viewsets.ModelViewSet):
    queryset = Patinete.objects.all()
    serializer_class = PatineteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def alquilar(self, request, pk=None):
        patinete = get_object_or_404(Patinete, numero=pk)

        esta_libre = patinete.alquiler_set.filter(fecha_entrega=None).count() == 0

        if not esta_libre:
            return Response('El recurso no está disponible', status=status.HTTP_404_NOT_FOUND)

        usuario = Usuario.objects.get(usuario=request.user)
        alquiler = Alquiler(patinete=patinete, fecha_desbloqueo=timezone.now(), usuario=usuario)
        alquiler.save()

        return Response(AlquilerSerializer(alquiler, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(detail=True, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def liberar(self, request, pk=None):
        patinete = get_object_or_404(Patinete, numero=pk)

        esta_libre = patinete.alquiler_set.filter(fecha_entrega=None).count() == 0

        if esta_libre:
            return Response('El recurso no está ocupado', status=status.HTTP_404_NOT_FOUND)

        alquiler = patinete.alquiler_set.get(fecha_entrega=None)
        self.check_object_permissions(request, alquiler)

        alquiler.fecha_entrega = timezone.now()
        delta = alquiler.fecha_entrega - alquiler.fecha_desbloqueo
        minutos_alquiler = int(delta.total_seconds() / 60)
        coste_final = patinete.precio_desbloqueo \
                      + minutos_alquiler * patinete.precio_minuto
        alquiler.coste_final = coste_final
        alquiler.usuario.debit -= float(coste_final)
        alquiler.save()
        alquiler.usuario.save()

        return Response(AlquilerSerializer(alquiler, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def patinetes_libres(self, request):
        patinetes_libres = Patinete.objects.exclude(Q(alquiler__isnull=False)
                                                    & Q(alquiler__fecha_entrega__isnull=True))
        serializer = self.get_serializer(patinetes_libres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def patinetes_ocupados(self, request):
        patinetes_ocupados = Patinete.objects.filter(Q(alquiler__isnull=False)
                                                    & Q(alquiler__fecha_entrega__isnull=True))
        serializer = self.get_serializer(patinetes_ocupados, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def top_ten(self,request):
        top_ten = Patinete.objects.annotate(alquileres=Count('alquiler__patinete')).order_by('-alquileres')[:10]
        serializer = self.get_serializer(top_ten, many=True)
        return Response(serializer.data)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['debit']

    @action(detail=False, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def top_three(self,request):
        top_three = Usuario.objects.annotate(alquileres=Count('alquiler__usuario')).order_by('-alquileres')[:1]
        serializer = self.get_serializer(top_three, many=True)
        return Response(serializer.data)

class AlquilerViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        alquileres = Alquiler.objects.all()
        user = self.request.user

        if not user.is_staff:
            usuario = Usuario.objects.get(usuario=user)
            alquileres = alquileres.filter(usuario=usuario)

        return alquileres
