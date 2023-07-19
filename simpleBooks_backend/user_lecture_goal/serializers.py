
from rest_framework import serializers
from .models import UserLectureGoal


class UserLectureGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLectureGoal
        fields = '__all__'

