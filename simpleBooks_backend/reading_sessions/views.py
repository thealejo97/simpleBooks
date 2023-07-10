from rest_framework import viewsets
from .models import ReadingSession
from .serializers import ReadingSessionSerializer

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
