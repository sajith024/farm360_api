from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models import CharField, EmailField, ImageField, DateTimeField
from django.db.models import OneToOneField, ForeignKey, CASCADE

from .manager import MyUserManager


class Country(Model):
    name = CharField(max_length=150)
    code = CharField(max_length=3, unique=True)
    flag = ImageField(upload_to="country/flags/")

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


class PhoneCode(Model):
    country = ForeignKey(Country, on_delete=CASCADE, related_name="phone_code")
    code = CharField(max_length=3)
    
    def __str__(self) -> str:
        return f"{self.country.code} {self.code}"


class Farm360UserProfile(Model):
    user = OneToOneField(Farm360User, on_delete=CASCADE, related_name="profile")
    image = ImageField(upload_to="user/profile/image", default="", blank=True)
    phone_code = ForeignKey(PhoneCode, on_delete=CASCADE, related_name="users")
    phone_number = CharField(max_length=15, blank=True, default="")
    role = ForeignKey(Role, on_delete=CASCADE, related_name="users")
    language = ForeignKey(Language, on_delete=CASCADE, related_name="users")
    country = ForeignKey(Country, on_delete=CASCADE, related_name="users")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile {self.user.email}"
