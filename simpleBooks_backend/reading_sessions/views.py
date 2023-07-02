from rest_framework import viewsets
from .models import ReadingSession
from .serializers import ReadingSessionSerializer

class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer