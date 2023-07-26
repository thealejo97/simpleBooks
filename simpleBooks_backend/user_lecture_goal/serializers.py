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
            'goal_velocidad_lectura',
            'goal_page_per_day_last_week',
            'goal_sessions_per_day_sum_last_week',
            'goal_readed_hours_day_last_week',
            'goal_book_per_year',
            'estadisticas',
        )


    # Agregamos un método "get_estadisticas" para obtener las estadísticas
    def get_estadisticas(self, obj):
        estadisticas = ReadingSession.obtener_estadisticas(obj.user.id)
        return estadisticas
