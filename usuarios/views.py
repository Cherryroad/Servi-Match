from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework import viewsets

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Sum

@csrf_exempt
@api_view(['POST'])
def vista_login(request):
    correo = request.data.get('correo')
    password = request.data.get('password')

    if not correo or not password:
        return Response({'error': 'Correo y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, usuario.password):
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'id': usuario.id,  # ← CAMBIO AQUÍ
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'correo': usuario.correo,
        'es_trabajador': usuario.es_trabajador
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def vista_usuario_detalle(request, usuario_id):
    try:
        usuario = Usuario.objects.select_related(
            'comuna__ciudad__region__pais'
        ).get(id=usuario_id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        data = serializer.data

        # Agrega campo "direccion" legible
        if usuario.comuna:
            data['direccion'] = f"{usuario.comuna.nombre_comuna}, {usuario.comuna.ciudad.nombre_ciudad}, {usuario.comuna.ciudad.region.nombre_region}, {usuario.comuna.ciudad.region.pais.nombre_pais}"
        else:
            data['direccion'] = "Sin dirección registrada"

        return Response(data)

    elif request.method == 'PUT':
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Usuario actualizado correctamente'})
        return Response(serializer.errors, status=400)



def vista_registrar_trabajador(request):
    return render(request, 'registrar-trabajador.html')


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer


class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer


class TipoEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = TipoEspecialidad.objects.all()
    serializer_class = TipoEspecialidadSerializer


class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TrabajadorReadSerializer
        return TrabajadorWriteSerializer

    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            return self.queryset.filter(usuario_id=usuario_id)
        return self.queryset.all()


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    @action(detail=True, methods=['post'])
    def subir_imagenes(self, request, pk=None):
        servicio = self.get_object()
        imagenes = request.FILES.getlist('imagenes')
        for img in imagenes:
            ImagenServicio.objects.create(servicio=servicio, imagen=img)
        return Response({'mensaje': 'Imágenes subidas con éxito'}, status=status.HTTP_201_CREATED)


class PlanServicioViewSet(viewsets.ModelViewSet):
    queryset = PlanServicio.objects.all()
    serializer_class = PlanServicioSerializer

    def get_queryset(self):
        servicio_id = self.request.query_params.get('servicio')
        if servicio_id:
            return self.queryset.filter(servicio_id=servicio_id)
        return self.queryset.all()



class TipoPagoViewSet(viewsets.ModelViewSet):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer


class BoletaViewSet(viewsets.ModelViewSet):
    queryset = Boleta.objects.all()
    serializer_class = BoletaSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

@api_view(['GET'])
def api_usuarios_por_comuna(request):
    data = Comuna.objects.annotate(total=Count('usuario')).values('nombre_comuna', 'total')
    return Response(list(data))

@api_view(['GET'])
def api_trabajadores_por_especialidad(request):
    data = Especialidad.objects.annotate(total=Count('trabajador')).values('nombre_esp', 'total')
    return Response(list(data))

@api_view(['GET'])
def api_servicios_mas_ofrecidos(request):
    data = Servicio.objects.annotate(total=Count('trabajadores')).values('nombre_serv', 'total')
    return Response(list(data))

@api_view(['GET'])
def api_boletas_por_tipo_pago(request):
    data = TipoPago.objects.annotate(total=Count('boleta')).values('descripcion', 'total')
    return Response(list(data))

@api_view(['GET'])
def api_monto_total_por_usuario(request):
    data = Boleta.objects.values('usuario__nombre').annotate(total=Sum('monto'))
    return Response(list(data))
