from rest_framework import serializers
from .models import UserLectureGoal
from ..reading_sessions.models import ReadingSession


class UserLectureGoalSerializer(serializers.ModelSerializer):

    # Agregamos esta línea para que la clase "MethodSerializer" pueda ser encontrada
    estadisticas = serializers.SerializerMethodField()
    class Meta:
        model = UserLectureGoal
        fields = (
            'id',
            'user',
            'goal_page_per_day',
            'goal_reading_speed',
            'goal_sessions_per_day',
            'goal_hours_per_day',
            'goal_book_per_year',
            'creation_date',
            'estadisticas',
        )


    # Agregamos un método "get_estadisticas" para obtener las estadísticas
    def get_estadisticas(self, obj):
        estadisticas = ReadingSession.obtener_estadisticas(obj.user.id)
        return estadisticas
