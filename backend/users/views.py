from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Endpoint de registro: POST /api/auth/register/
    Corpo esperado: { "username": "...", "handle": "...", "password": "..." }
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """
    Endpoint do usuário logado: GET/PATCH /api/auth/me/
    Usado para ver e editar o próprio perfil (bio, avatar, handle).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user