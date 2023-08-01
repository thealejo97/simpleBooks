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
            goal = self.get_queryset().filter(user__id=user_id).last()
            if goal:
                serializer = self.get_serializer(goal)
                return Response(serializer.data)
            else:
                return Response({})
        else:
            return Response({})

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        if user_id:
            # Eliminar registros anteriores del mismo usuario antes de crear uno nuevo
            UserLectureGoal.objects.filter(user__id=user_id).delete()
            serializer.save()
        else:
            return Response({'error': 'No se proporcionó un usuario válido.'}, status=status.HTTP_400_BAD_REQUEST)