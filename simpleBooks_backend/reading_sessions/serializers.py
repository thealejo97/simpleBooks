from rest_framework import serializers
from .models import ReadingSession
from ..users.serializers import UserSerializer


class ReadingSessionSerializer(serializers.ModelSerializer):
    queryset = ReadingSession.objects.all().order_by('-creation_date')
    class Meta:
        model = ReadingSession
        fields = [
            'id',
            'time_of_reading',
            'creation_date',
            'readed_pages',
            'comment',
            'user',
            'book'
        ]