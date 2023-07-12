from rest_framework import serializers
from .models import User
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, username):
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'username': self.validated_data.get('username', ''),
        }

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.save()
        return user