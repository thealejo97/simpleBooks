from django.db import models

from simpleBooks_backend.books.models import Book
from ..users.models import User
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Avg, Max, Min


class ReadingSession(models.Model):
    time_of_reading = models.TimeField()
    creation_date = models.TimeField(auto_now_add=True)
    readed_pages = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    @staticmethod
    def obtener_hojas_leidas_por_minuto(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario).aggregate(
            tiempo_total=Sum(ExpressionWrapper(F("time_of_reading"), output_field=DurationField())),
            hojas_leidas=Sum("readed_pages"),
        )
        if not sesiones_lectura:
            return 0
        tiempo_total = sesiones_lectura["tiempo_total"]
        hojas_leidas = sesiones_lectura["hojas_leidas"]

        if tiempo_total and hojas_leidas:
            hojas_por_minuto = hojas_leidas / (tiempo_total.total_seconds() / 60)
            hojas_por_minuto = round(hojas_por_minuto, 2)  # Redondear a 2 decimales
        else:
            hojas_por_minuto = 0

        return hojas_por_minuto

    @staticmethod
    def obtener_hojas_leidas_promedio_por_sesion(usuario_id):
        usuario = User.objects.get(id=usuario_id)

        hojas_promedio = ReadingSession.objects.filter(user=usuario).aggregate(
            hojas_promedio=Avg("readed_pages")
        )["hojas_promedio"]
        if not hojas_promedio:
            return 0
        return hojas_promedio
    @staticmethod
    def obtener_total_sesiones_lectura(usuario_id):
        return ReadingSession.objects.filter(user_id=usuario_id).count()
    @staticmethod
    def obtener_tiempo_total_lectura(usuario_id):
        tiempo_total = ReadingSession.objects.filter(user_id=usuario_id).aggregate(
            tiempo_total=Sum("time_of_reading")
        )["tiempo_total"]
        if not tiempo_total:
            return 0
        return (tiempo_total.total_seconds() / 60)
    @staticmethod
    def obtener_total_hojas_leidas(usuario_id):
        total_hojas_leidas = ReadingSession.objects.filter(user_id=usuario_id).aggregate(
            total_hojas_leidas=Sum("readed_pages")
        )["total_hojas_leidas"]
        if not total_hojas_leidas:
            return 0
        return total_hojas_leidas
    @staticmethod
    def obtener_promedio_tiempo_lectura_por_sesion(usuario_id):
        promedio_tiempo_lectura = ReadingSession.objects.filter(user_id=usuario_id).aggregate(
            promedio_tiempo=Avg("time_of_reading")
        )["promedio_tiempo"]
        if not promedio_tiempo_lectura:
            return 0
        return (promedio_tiempo_lectura / 60)
    @staticmethod
    def obtener_duracion_sesion_mas_larga(usuario_id):
        duracion_sesion_mas_larga = ReadingSession.objects.filter(user_id=usuario_id).aggregate(
            duracion_sesion_mas_larga=Max("time_of_reading")
        )["duracion_sesion_mas_larga"]
        if not duracion_sesion_mas_larga:
            return 0
        return duracion_sesion_mas_larga
    @staticmethod
    def obtener_duracion_sesion_mas_corta(usuario_id):
        duracion_sesion_mas_corta = ReadingSession.objects.filter(user_id=usuario_id).aggregate(
            duracion_sesion_mas_corta=Min("time_of_reading")
        )["duracion_sesion_mas_corta"]
        if not duracion_sesion_mas_corta:
            return 0
        return duracion_sesion_mas_corta