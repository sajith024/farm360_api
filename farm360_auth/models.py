from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models import CharField, EmailField
from django.db.models import OneToOneField, ForeignKey, CASCADE

from .manager import MyUserManager


class Country(Model):
    name = CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Language(Model):
    name = CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Role(Model):
    name = CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Farm360User(AbstractUser):
    username = None
    email = EmailField(
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self) -> str:
        return self.email


class Farm360UserProfile(Model):
    user = OneToOneField(Farm360User, on_delete=CASCADE, related_name="profile")
    phone_number = CharField(max_length=15, blank=True, default="")
    role = ForeignKey(Role, on_delete=CASCADE, related_name="users")
    language = ForeignKey(Language, on_delete=CASCADE, related_name="users")
    country = ForeignKey(Country, on_delete=CASCADE, related_name="users")

    def __str__(self) -> str:
        return f"Profile {self.user.email}"
