from django.core.management.base import BaseCommand
from usuarios.models import *
from django.contrib.auth.hashers import make_password
from datetime import date, datetime
import random
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Carga datos demo para todos los modelos'

    def handle(self, *args, **kwargs):
        print("Borrando datos existentes...")

        # Borrado en orden para evitar errores por referencias
        Mensaje.objects.all().delete()
        Chat.objects.all().delete()
        Cita.objects.all().delete()
        Boleta.objects.all().delete()
        PlanServicio.objects.all().delete()
        Servicio.objects.all().delete()
        Trabajador.objects.all().delete()
        Usuario.objects.all().delete()
        Comuna.objects.all().delete()
        Ciudad.objects.all().delete()
        Region.objects.all().delete()
        Pais.objects.all().delete()
        Especialidad.objects.all().delete()
        TipoServicio.objects.all().delete()
        TipoPago.objects.all().delete()

        print("Creando registros nuevos...")

        pais = Pais.objects.create(nombre_pais="Chile")
        region = Region.objects.create(nombre_region="Metropolitana", pais=pais)
        ciudad = Ciudad.objects.create(nombre_ciudad="Santiago", region=region)
        comuna = Comuna.objects.create(nombre_comuna="San Bernardo", ciudad=ciudad)

        esp1 = Especialidad.objects.create(nombre_esp="Albañil")
        esp2 = Especialidad.objects.create(nombre_esp="Electricista")
        tipo1 = TipoServicio.objects.create(nombre_tipo="Reparación")
        tipo2 = TipoServicio.objects.create(nombre_tipo="Instalación")
        pago1 = TipoPago.objects.create(descripcion="Efectivo")
        pago2 = TipoPago.objects.create(descripcion="Transferencia")

        fake_image = ContentFile(b"fake image data", name='fake.jpg')

        usuarios = []
        trabajadores = []

        # ✅ Cliente principal con RUT único
        rut_unico = f"11111111-{datetime.now().strftime('%H%M%S')}"
        cliente_principal = Usuario.objects.create(
            rut=rut_unico,
            nombre="Juan",
            apellido="Cliente",
            correo="juan_cliente@mail.com",
            telefono="912345678",
            fecha_nac=date(1995, 1, 1),
            comuna=comuna,
            password=make_password("12345678"),
            foto_perfil=fake_image
        )
        usuarios.append(cliente_principal)

        # Clientes demo adicionales
        for i in range(2):  # Total: 3 clientes
            rut_cliente = f"1111111{i+random.randint(100,999)}-K"
            u = Usuario.objects.create(
                rut=rut_cliente,
                nombre=f"Cliente{i+1}",
                apellido="Demo",
                correo=f"cliente{i+1}@mail.com",
                telefono="912345678",
                fecha_nac=date(1995, 1, i+2),
                comuna=comuna,
                password=make_password("1234"),
                foto_perfil=fake_image
            )
            usuarios.append(u)

        # Trabajadores
        for i in range(3):
            rut_trab = f"2222222{i+random.randint(100,999)}-K"
            u = Usuario.objects.create(
                rut=rut_trab,
                nombre=f"Trabajador{i}",
                apellido="Demo",
                correo=f"trabajador{i}@mail.com",
                telefono="923456789",
                fecha_nac=date(1990, 6, i+1),
                comuna=comuna,
                password=make_password("1234"),
                foto_perfil=fake_image
            )
            usuarios.append(u)

            t = Trabajador.objects.create(
                usuario=u,
                especialidad=random.choice([esp1, esp2]),
                estado_verificado=True,
                foto_cedula=fake_image,
                foto_cedula_atras=fake_image,
                foto_autoretrato=fake_image
            )
            trabajadores.append(t)

        servicio_nombres = [
            "Instalación de luces",
            "Reparación de enchufes",
            "Arreglo de cañerías",
            "Pintura interior",
            "Cambio de cerámicas",
            "Instalación de muebles",
            "Servicio de gasfitería",
            "Mantenimiento eléctrico",
            "Revisión de calefacción",
            "Construcción de terraza"
        ]

        servicios = []
        for nombre in servicio_nombres:
            s = Servicio.objects.create(
                nombre_serv=nombre,
                tipo=random.choice([tipo1, tipo2]),
                descripcion_breve="Servicio profesional realizado con calidad garantizada."
            )
            s.trabajadores.set(random.sample(trabajadores, k=random.randint(1, 3)))
            servicios.append(s)

            PlanServicio.objects.create(
                servicio=s,
                nombre_plan="Plan Básico",
                precio=random.randint(20000, 60000),
                duracion="1 día",
                incluye="Materiales básicos\nMano de obra\nGarantía 3 meses",
                descripcion_breve="Ideal para tareas pequeñas"
            )

        for _ in range(10):
            Boleta.objects.create(
                servicio=random.choice(servicios),
                usuario=random.choice(usuarios[:3]),  # Solo clientes
                monto=random.randint(20000, 80000),
                tipo_pago=random.choice([pago1, pago2])
            )

        print("✅ Datos demo cargados correctamente.")
