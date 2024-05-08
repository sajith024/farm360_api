from django.contrib import admin

from .models import (
    Country,
    Language,
    Role,
    Farm360User,
    Farm360UserProfile,
)

# Register your models here.
admin.site.register(
    (
        Country,
        Language,
        Role,
        Farm360User,
        Farm360UserProfile,
    )
)
