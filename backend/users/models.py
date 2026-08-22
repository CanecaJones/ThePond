from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ThePondUserManager(UserManager):
    """
    Manager customizado — remove a dependência do campo email
    que o UserManager padrão do Django exige.
    """

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("O username é obrigatório.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    handle = models.CharField(
        max_length=30,
        unique=True,
        help_text="Nome de exibição @handle, editável pelo usuário depois."
    )
    bio = models.CharField(max_length=160, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_mod = models.BooleanField(default=False)

    email = None
    REQUIRED_FIELDS = ["handle"]

    objects = ThePondUserManager()

    def __str__(self):
        return f"@{self.handle}"