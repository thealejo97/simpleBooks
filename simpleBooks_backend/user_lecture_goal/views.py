from rest_framework import viewsets
from simpleBooks_backend.user_lecture_goal.models import UserLectureGoal
from simpleBooks_backend.user_lecture_goal.serializers import UserLectureGoalSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserLectureGoalViewSet(viewsets.ModelViewSet):
    queryset = UserLectureGoal.objects.all()
    serializer_class = UserLectureGoalSerializer

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id')
        sessions = self.get_queryset().filter(user__id=user_id)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
