from rest_framework import generics, permissions, parsers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Follow
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Endpoint de registro: POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """
    Endpoint do usuário logado: GET/PATCH /api/auth/me/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_object(self):
        return self.request.user


class PublicProfileView(generics.RetrieveAPIView):
    """
    Perfil público de qualquer usuário: GET /api/auth/profile/<handle>/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "handle"
    queryset = User.objects.all()


class FollowToggleView(APIView):
    """
    POST /api/auth/follow/<handle>/ -> segue ou deixa de seguir (toggle)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, handle):
        try:
            target = User.objects.get(handle=handle)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if target == request.user:
            return Response({"detail": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
            return Response({"following": False})

        return Response({"following": True})