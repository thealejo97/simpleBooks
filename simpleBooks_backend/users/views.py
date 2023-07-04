from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_auth.views import LoginView
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        user_id = self.request.user.id
        user_email = self.request.user.username
        data = {
            'id': user_id,
            'user_email': user_email,
            'token': original_response.data['key']
        }
        original_response.data = data
        return original_response