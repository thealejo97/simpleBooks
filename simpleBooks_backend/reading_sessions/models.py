from collections import defaultdict

from django.db import models

from simpleBooks_backend.books.models import Book
from ..users.models import User
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Avg, Max, Min
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from collections import defaultdict
from django.utils import timezone

class ReadingSession(models.Model):
    time_of_reading = models.TimeField()
    creation_date = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    readed_pages = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    @staticmethod
    def obtener_estadisticas(usuario_id):
        """
        Campos:
            velocidad_lectura OK
            page_per_day_last_week OK
            page_per_day_avg_last_week OK
            sessions_per_day_last_week OK
            sessions_per_day_sum_last_week OK
            hours_last_week OK
            readed_hours_day_last_week OK
            books_per_year OK
        """
        estadisticas = {}

        if usuario_id:
                ####velocidad_lectura
                hojas_leidas_por_minuto = ReadingSession.obtener_hojas_leidas_por_minuto(usuario_id)
                estadisticas["velocidad_lectura"] = Decimal(hojas_leidas_por_minuto).quantize(Decimal('0.00'))
                ####HOJAS POR DIA
                hojas_leidas_por_dia = ReadingSession.obtener_hojas_leidas_por_dia(usuario_id)
                estadisticas["page_per_day_last_week"] = hojas_leidas_por_dia
                ####HOJAS POR DIA PROM
                if hojas_leidas_por_dia:
                    page_per_day_avg_last_week = Decimal(sum(hojas_leidas_por_dia.values()) / len(hojas_leidas_por_dia)).quantize(Decimal('0.00'))
                else:
                    page_per_day_avg_last_week = Decimal(0).quantize(Decimal('0.00'))
                estadisticas["page_per_day_avg_last_week"] = page_per_day_avg_last_week
                ####SESIONES POR DIA EN LA ULTIMA SEMANA
                sesiones_por_dia = ReadingSession.obtener_sesiones_por_dia(usuario_id)
                estadisticas["sessions_per_day_last_week"] = sesiones_por_dia
                ####SESIONES EN LA ULTIMA SEMANA
                if sesiones_por_dia:
                    sessions_per_day_sum_last_week = Decimal(sum(sesiones_por_dia.values())).quantize(Decimal('0.00'))
                else:
                    sessions_per_day_sum_last_week = Decimal(0).quantize(Decimal('0.00'))
                estadisticas["sessions_per_day_sum_last_week"] = sessions_per_day_sum_last_week

                ####HORAS POR DIA EN LA ULTIMA SEMANA
                horas_por_dia = ReadingSession.obtener_horas_por_dia(usuario_id)
                estadisticas["hours_last_week"] = horas_por_dia

                if horas_por_dia:
                    hours_readed = Decimal(sum(horas_por_dia.values())).quantize(Decimal('0.00'))
                    hours_int, minutes_decimal = divmod(hours_readed * 60, 60)
                    estadisticas["readed_hours_day_last_week"] = f"{hours_int:02}:{int(minutes_decimal):02}"
                else:
                    estadisticas["readed_hours_day_last_week"] = "00:00"

                estadisticas["books_per_year"] = ReadingSession.obtener_libros_en_ano(usuario_id)
        return estadisticas

##  METODOS ESTADISTICOS
    @staticmethod
    def obtener_libros_en_ano(usuario_id):
        current_year = datetime.now().year
        amount_books = Book.objects.filter(user_id=usuario_id, creation_date__year=current_year).count()
        return amount_books

    @staticmethod
    def obtener_horas_por_dia(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario)

        # Obtiene la fecha de hoy
        today = datetime.now().date()

        # Calcula la fecha de hace 8 días
        eight_days_ago = today - timedelta(days=7)

        # Crea una lista con las fechas desde hace 7 días
        date_list = [eight_days_ago + timedelta(days=x) for x in range(7)]

        # Use a defaultdict to track the number of hours per day
        horas_por_dia = defaultdict(int)

        # Populate hours count for each date
        for date in date_list:
            fecha_sesion = str(date)
            horas_por_dia[fecha_sesion] = 0

        for sesion in sesiones_lectura:
            fecha_sesion = str(sesion.creation_date.date())
            horas_por_dia[fecha_sesion] += sesion.time_of_reading.hour

        # Convert the defaultdict to a normal dictionary
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

        # Obtiene la fecha de hoy
        today = timezone.now().date()

        # Calcula la fecha de hace 8 días
        eight_days_ago = today - timedelta(days=7)

        # Crea una lista con las fechas desde hace 7 días
        date_list = [eight_days_ago + timedelta(days=x) for x in range(7)]

        # Use a defaultdict to track the number of sessions per day
        sesiones_por_dia = defaultdict(int)

        # Populate sessions count for each date
        for date in date_list:
            fecha_sesion = str(date)
            sesiones_por_dia[fecha_sesion] = 0

        for sesion in sesiones_lectura:
            fecha_sesion = str(sesion.creation_date.date())
            sesiones_por_dia[fecha_sesion] += 1

        # Convert the defaultdict to a normal dictionary
        sesiones_por_dia = dict(sesiones_por_dia)

        return sesiones_por_dia

    @staticmethod
    def obtener_hojas_leidas_por_dia(usuario_id):
        usuario = User.objects.get(id=usuario_id)
        sesiones_lectura = ReadingSession.objects.filter(user=usuario)

        # Obtiene la fecha de hoy
        today = timezone.now().date()

        # Calcula la fecha de hace 8 dias
        eight_days_ago = today - timedelta(days=6)

        # Crea una lista con las fechas desde hace 6 dias
        date_list = [eight_days_ago + timedelta(days=x) for x in range(6)]

        # Use a defaultdict to track the pages read per day
        paginas_por_dia = defaultdict(int)

        # Populate pages read for each date
        for date in date_list:
            fecha_sesion = date.strftime('%d-%b')  # Format date as "dd-MMM" (e.g., "26-JUL")
            paginas_por_dia[fecha_sesion] = 0

        for sesion in sesiones_lectura:
            fecha_sesion = sesion.creation_date.date().strftime('%d-%b')  # Format date as "dd-MMM" (e.g., "26-JUL")
            paginas_por_dia[fecha_sesion] += sesion.readed_pages

        # Create the JSON response using the populated pages per day
        json_respuesta = {fecha: paginas for fecha, paginas in paginas_por_dia.items()}

        return json_respuesta

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