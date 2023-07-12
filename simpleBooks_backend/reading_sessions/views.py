from rest_framework import viewsets
from .models import ReadingSession
from .serializers import ReadingSessionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



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

class ReadingSessionStatistics(APIView):
    def post(self, request):
        estadisticas = {}
        usuario_id = request.data.get("user_id")
        estadisticas["hojas_leidas_por_minuto"] = ReadingSession.obtener_hojas_leidas_por_minuto(usuario_id)
        estadisticas["hojas_leidas_promedio_por_sesion"] = ReadingSession.obtener_hojas_leidas_promedio_por_sesion(usuario_id)
        estadisticas["total_sesiones_lectura"] = ReadingSession.obtener_total_sesiones_lectura(usuario_id)
        estadisticas["tiempo_total_lectura"] = ReadingSession.obtener_tiempo_total_lectura(usuario_id)
        estadisticas["total_hojas_leidas"] = ReadingSession.obtener_total_hojas_leidas(usuario_id)
        estadisticas["promedio_tiempo_lectura_por_sesion"] = ReadingSession.obtener_promedio_tiempo_lectura_por_sesion(usuario_id)
        estadisticas["duracion_sesion_mas_larga"] = ReadingSession.obtener_duracion_sesion_mas_larga(usuario_id)
        estadisticas["duracion_sesion_mas_corta"] = ReadingSession.obtener_duracion_sesion_mas_corta(usuario_id)

        return Response(estadisticas)