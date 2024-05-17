import re

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ImageField,
    ModelSerializer,
    SerializerMethodField,
)

from .models import (
    CommunityComment,
    CommunityCommentImage,
    CommunityQuery,
    CommunityQueryImage,
)


class CommunityQueryImageSerializer(ModelSerializer):
    class Meta:
        model = CommunityQueryImage
        fields = "__all__"


class CommunityCommentImageSerializer(ModelSerializer):
    class Meta:
        model = CommunityCommentImage
        fields = "__all__"


class CommunityQuerySerializer(ModelSerializer):
    class Meta:
        model = CommunityQuery
        fields = (
            "id",
            "title",
            "description",
            "query_type",
        )


class CommunityCommentSerializer(ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = (
            "id",
            "description",
            "query",
            "main",
        )


class CommunityCreatedUserDetail(ModelSerializer):
    image = ImageField(source="profile.image")
    country = CharField(source="profile.country.name")
    role = CharField(source="profile.role.name")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "image",
            "country",
            "role",
        )


class CommunityQueryDetailSerializer(ModelSerializer):
    created_by = CommunityCreatedUserDetail()
    images = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = CommunityQuery
        fields = (
            "id",
            "title",
            "description",
            "query_type",
            "created_at",
            "created_by",
            "images",
            "replies",
        )

    def get_images(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(community_image.image.url)
            for community_image in obj.images.all()
        ]

    def get_replies(self, obj):
        return obj.comments.filter(
            ~Q(created_by__profile__role__name="Admin") & Q(main__isnull=True)
        ).count()


class CommunityCommentDetailSerializer(ModelSerializer):
    created_by = CommunityCreatedUserDetail()
    threads = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = CommunityComment
        fields = (
            "id",
            "description",
            "images",
            "created_at",
            "created_by",
            "threads",
        )

    def get_threads(self, obj):
        serializer = CommunityCommentDetailSerializer(
            instance=obj.threads.all(),
            many=True,
            context=self.context,
        )
        return serializer.data

    def get_images(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(comment_image.image.url)
            for comment_image in obj.images.all()
        ]
