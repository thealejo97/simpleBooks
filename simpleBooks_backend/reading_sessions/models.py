from collections import defaultdict

from django.db import models

from simpleBooks_backend.books.models import Book
from ..users.models import User
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Avg, Max, Min
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime


class ReadingSession(models.Model):
    time_of_reading = models.TimeField()
    creation_date = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    readed_pages = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    @staticmethod
    def obtener_estadisticas(usuario_id):
        estadisticas = {}

        estadisticas["hojas_leidas_promedio_por_sesion"] = Decimal(ReadingSession.obtener_hojas_leidas_promedio_por_sesion(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["total_sesiones_lectura"] = Decimal(ReadingSession.obtener_total_sesiones_lectura(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["tiempo_total_lectura"] = Decimal(ReadingSession.obtener_tiempo_total_lectura(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["total_hojas_leidas"] = Decimal(ReadingSession.obtener_total_hojas_leidas(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["promedio_tiempo_lectura_por_sesion"] = ReadingSession.obtener_promedio_tiempo_lectura_por_sesion(usuario_id)
        estadisticas["duracion_sesion_mas_larga"] = ReadingSession.obtener_duracion_sesion_mas_larga(usuario_id)
        estadisticas["duracion_sesion_mas_corta"] = ReadingSession.obtener_duracion_sesion_mas_corta(usuario_id)

        ####
        estadisticas["velocidad_lectura"] = Decimal(ReadingSession.obtener_hojas_leidas_por_minuto(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["page_per_day"] = ReadingSession.obtener_hojas_leidas_por_dia(usuario_id)
        estadisticas["page_per_day_avg"] = Decimal(sum(estadisticas["page_per_day"].values())/len(estadisticas["page_per_day"])).quantize(Decimal('0.00'))
        estadisticas["sessions_per_day"] = ReadingSession.obtener_sesiones_por_dia(usuario_id)
        estadisticas["sessions_per_day_avg"] = Decimal(sum(estadisticas["sessions_per_day"].values())/len(estadisticas["sessions_per_day"])).quantize(Decimal('0.00'))
        estadisticas["hours_per_day"] = ReadingSession.obtener_horas_por_dia(usuario_id)
        # Supongamos que tienes el promedio de horas por día en la variable `hours_per_day_avg` (este valor debe ser reemplazado por el que corresponda)
        hours_per_day_avg = Decimal(sum(estadisticas["hours_per_day"].values()) / len(estadisticas["hours_per_day"])).quantize(Decimal('0.00'))
        # Dividimos el número decimal en partes enteras y decimales, usando divmod()
        hours_int, minutes_decimal = divmod(hours_per_day_avg * 60, 60)
        # Formateamos las horas y los minutos con ceros a la izquierda si es necesario
        estadisticas["hours_per_day_avg"] = f"{hours_int:02}:{int(minutes_decimal):02}"
        estadisticas["books_per_year"] = ReadingSession.obtener_libros_en_ano(usuario_id)
        return estadisticas


    @staticmethod
    def obtener_libros_en_ano(usuario_id):
        current_year = datetime.now().year
        amount_books = Book.objects.filter(user_id=usuario_id, creation_date__year=current_year).count()
        return amount_books
    @staticmethod
    def obtener_horas_por_dia(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario)

        if not sesiones_lectura:
            return {}

        # Usamos una lista de tuplas para realizar el seguimiento de las horas de sesiones por día
        horas_por_dia = defaultdict(int)

        for sesion in sesiones_lectura:
            # Convertimos la fecha a un string en formato yyyy-mm-dd para agrupar las sesiones por día
            fecha_sesion = str(sesion.creation_date.date())

            # Sumamos las horas de la sesión al día correspondiente
            horas_por_dia[fecha_sesion] += sesion.time_of_reading.hour

        # Convertimos el defaultdict a un diccionario normal
        horas_por_dia = dict(horas_por_dia)

        return horas_por_dia

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
    def obtener_sesiones_por_dia(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario)

        if not sesiones_lectura:
            return {}

        # Usamos una lista de tuplas para realizar el seguimiento del número de sesiones por día
        sesiones_por_dia = defaultdict(int)

        for sesion in sesiones_lectura:
            # Convertimos la fecha a un string en formato yyyy-mm-dd para agrupar las sesiones por día
            fecha_sesion = str(sesion.creation_date.date())

            # Incrementamos el contador de sesiones para el día correspondiente
            sesiones_por_dia[fecha_sesion] += 1

        # Convertimos el defaultdict a un diccionario normal
        sesiones_por_dia = dict(sesiones_por_dia)

        return sesiones_por_dia

    @staticmethod
    def obtener_hojas_leidas_por_dia(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario)

        if not sesiones_lectura:
            return {}

        # Usamos una lista de tuplas para realizar el seguimiento de las páginas leídas por día
        paginas_por_dia = defaultdict(int)

        for sesion in sesiones_lectura:
            # Convertimos la fecha a un string en formato yyyy-mm-dd para agrupar las sesiones por día
            fecha_sesion = str(sesion.creation_date.date())

            # Sumamos las páginas leídas al día correspondiente
            paginas_por_dia[fecha_sesion] += sesion.readed_pages

        # Convertimos el defaultdict a una lista de tuplas (fecha, paginas)
        lista_paginas_por_dia = list(paginas_por_dia.items())

        # Ordenamos la lista de tuplas por las fechas en orden descendente (de la más reciente a la más antigua)
        lista_paginas_por_dia.sort(reverse=True)

        # Construimos el JSON de respuesta utilizando la lista ordenada
        json_respuesta = {fecha: paginas for fecha, paginas in lista_paginas_por_dia}

        return json_respuesta
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
            return Decimal(0).quantize(Decimal('0.00'))

        # Convertir promedio_tiempo_lectura a minutos (decimal o flotante)
        promedio_tiempo_minutos = promedio_tiempo_lectura.total_seconds() / 60

        # Redondear a 2 decimales y convertir a Decimal
        return Decimal(promedio_tiempo_minutos).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
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