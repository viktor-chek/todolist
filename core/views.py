from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from core.serializers import RegistrationSerializer
from core.serializers import LoginSerializer
from core.serializers import ProfileSerializer
from core.serializers import UpdatePasswordSerializer

USER_MODEL = get_user_model()


class RegistrationView(CreateAPIView):
    """Представления страницы регистрации"""
    model = USER_MODEL
    serializer_class = RegistrationSerializer


class LoginView(GenericAPIView):
    """Представления страницы авторизации"""
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    """Представления страницы профиля"""
    serializer_class = ProfileSerializer
    queryset = USER_MODEL.objects.all()

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    """Представления страницы обновления пароля пользователя"""
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
