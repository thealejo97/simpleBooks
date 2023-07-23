from rest_framework import viewsets
from simpleBooks_backend.user_lecture_goal.models import UserLectureGoal
from simpleBooks_backend.user_lecture_goal.serializers import UserLectureGoalSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserLectureGoalViewSet(viewsets.ModelViewSet):
    queryset = UserLectureGoal.objects.all()
    serializer_class = UserLectureGoalSerializer

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            goal = self.get_queryset().filter(user__id=user_id).order_by('-creation_date').first()
            print("Retornando")
            if goal:
                serializer = self.get_serializer(goal)
                return Response(serializer.data)
            else:
                return Response({})
        else:
            return Response({})
