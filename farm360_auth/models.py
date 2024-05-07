from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(unique=True)

    def __str__(self) -> str:
        return self.name


class Farm360User(AbstractUser):
    pass