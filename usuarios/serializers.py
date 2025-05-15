from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'

class TipoEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEspecialidad
        fields = '__all__'

class PlanServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanServicio
        fields = '__all__'

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = '__all__'

class ImagenServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenServicio
        fields = ['id', 'imagen']

class ServicioSerializer(serializers.ModelSerializer):
    tipo = serializers.StringRelatedField()
    planes = PlanServicioSerializer(many=True, read_only=True)
    imagenes = ImagenServicioSerializer(many=True, read_only=True)

    class Meta:
        model = Servicio
        fields = '__all__'

class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'

# SERIALIZADORES DE TRABAJADOR

# → para escribir (POST/PUT)
class TrabajadorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

# → para leer (GET, con usuario y especialidad detallados)
class TrabajadorReadSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    especialidad = EspecialidadSerializer()
    servicios = ServicioSerializer(many=True, read_only=True)

    class Meta:
        model = Trabajador
        fields = '__all__'
