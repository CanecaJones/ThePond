from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de leitura — usado para retornar dados públicos do usuário
    (perfil, resposta de registro, etc.)
    """
    class Meta:
        model = User
        fields = ["id", "username", "handle", "bio", "avatar", "is_mod", "date_joined"]
        read_only_fields = ["id", "is_mod", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer usado apenas no registro — recebe senha e valida ela.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "handle", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["id", "follower", "created_at"]