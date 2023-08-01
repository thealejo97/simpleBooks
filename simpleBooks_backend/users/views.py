from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, CustomRegisterSerializer
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.views import APIView
from simpleBooks_backend.users.serializers import ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import smtplib
from email.mime.text import MIMEText


from ..settings import DOMINIO


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

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer



class CustomChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username:
            return Response({'detail': 'El campo "username" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password:
            return Response({'detail': 'El campo "new_password" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'El usuario con el nombre de usuario proporcionado no existe.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            # if not user.check_password(old_password):
            #     return Response({'detail': 'La contraseña actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            # Si estás usando Django Rest Framework Token Authentication, actualiza el token
            try:
                token = Token.objects.get(user=user)
                token.delete()
                Token.objects.create(user=user)
            except Token.DoesNotExist:
                pass

            return Response({'detail': 'La contraseña ha sido cambiada exitosamente.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

@api_view(['POST'])
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        user = get_object_or_404(User, username=email)
        print(user)

        # Generar el token utilizando el método que definimos en el modelo User
        reset_token = user.generate_reset_token()

        reset_url_resto = f'reset_password/?token={reset_token}'
        reset_url = DOMINIO + reset_url_resto
        print(reset_url)


        # Crear el mensaje codificado en formato UTF-8
        subject = 'Reseteo de Contraseña'
        message = f'Hola {user.username}, para resetear tu contraseña, haz clic en el siguiente enlace: {reset_url}'
        msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = 'fakethealejo97@gmail.com'
        msg['To'] = email

        # Enviar el mensaje utilizando smtplib
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("logueando")
            server.login('thealejo97@gmail.com', 'Alejandroreyok1')
            print("Enviando ...")
            server.send_message(msg)
            print("Enviado")

        return Response({'message': 'Se ha enviado un correo con las instrucciones para resetear tu contraseña.'})