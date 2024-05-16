from django.contrib import admin

from .models import (
    CommunityQuery,
    CommunityQueryImage,
    CommunityComment,
    CommunityCommentImage,
)

# Register your models here.
admin.site.register(
    (
        CommunityQuery,
        CommunityQueryImage,
        CommunityComment,
        CommunityCommentImage,
    )
)
