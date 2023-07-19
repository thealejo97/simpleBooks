from rest_framework import viewsets
from .models import ReadingSession
from .serializers import ReadingSessionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal



class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def perform_create(self, serializer):
        instance = serializer.save()  # Guardar la instancia de ReadingSession
        book = instance.book
        total_pages = book.total_pages
        pages_old = int(total_pages * (int(book.reading_status_porcentaje)/100))
        total_pages_readed = pages_old + instance.readed_pages
        percentage = (total_pages_readed / total_pages) * 100

        book.reading_status_porcentaje = int(percentage)
        book.save()

    @action(detail=False, methods=['GET'])
    def by_user_and_book(self, request):
        user_id = request.query_params.get('user_id')
        book_id = request.query_params.get('book_id')
        sessions = self.get_queryset().filter(user__id=user_id, book__id=book_id)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

class ReadingSessionStatistics(APIView):
    def post(self, request):
        estadisticas = {}
        usuario_id = request.data.get("user_id")
        estadisticas["hojas_leidas_por_minuto"] = Decimal(ReadingSession.obtener_hojas_leidas_por_minuto(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["hojas_leidas_promedio_por_sesion"] = Decimal(ReadingSession.obtener_hojas_leidas_promedio_por_sesion(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["total_sesiones_lectura"] = Decimal(ReadingSession.obtener_total_sesiones_lectura(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["tiempo_total_lectura"] = Decimal(ReadingSession.obtener_tiempo_total_lectura(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["total_hojas_leidas"] = Decimal(ReadingSession.obtener_total_hojas_leidas(usuario_id)).quantize(Decimal('0.00'))
        estadisticas["promedio_tiempo_lectura_por_sesion"] = ReadingSession.obtener_promedio_tiempo_lectura_por_sesion(usuario_id)
        estadisticas["duracion_sesion_mas_larga"] = ReadingSession.obtener_duracion_sesion_mas_larga(usuario_id)
        estadisticas["duracion_sesion_mas_corta"] = ReadingSession.obtener_duracion_sesion_mas_corta(usuario_id)

        ####
        estadisticas["page_per_day"] = ReadingSession.obtener_hojas_leidas_por_dia(usuario_id)

        return Response(estadisticas)