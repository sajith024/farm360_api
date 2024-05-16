import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, SerializerMethodField, ImageField
from rest_framework.serializers import ModelSerializer

from .models import (
    CommunityQuery,
    CommunityQueryImage,
    CommunityComment,
    CommunityCommentImage,
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


class CommunityQueryDetailSerializer(ModelSerializer):
    first_name = CharField(source="created_by.first_name")
    last_name = CharField(source="created_by.last_name")
    profile_image = ImageField(source="created_by.profile.image")
    country = CharField(source="created_by.profile.country.name")
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
            "first_name",
            "last_name",
            "profile_image",
            "country",
            "images",
            "replies",
        )

    def get_images(self, obj):
        community_images = obj.images.all()
        request = self.context.get("request")
        images = [
            request.build_absolute_uri(community_image.image.url)
            for community_image in community_images
        ]
        return images

    def get_replies(self, obj):
        return obj.comments.count()


class CommunityQueryCommentDetailSerializer(ModelSerializer):
    first_name = CharField(source="created_by.first_name")
    last_name = CharField(source="created_by.last_name")
    threads = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = CommunityComment
        fields = (
            "id",
            "description",
            "images",
            "created_at",
            "first_name",
            "last_name",
            "threads",
        )

    def get_threads(self, obj):
        threads = obj.threads.all()
        serializer = CommunityQueryCommentDetailSerializer(instance=threads, many=True)
        return serializer.data

    def get_images(self, obj):
        comment_images = obj.images.all()
        request = self.context.get("request")
        images = [
            request.build_absolute_uri(comment_image.image.url)
            for comment_image in comment_images
        ]
        return images
