from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CommunityQueryDetailViewSet,
    CommunityCommentDetailViewset,
    CommunityQueryViewSet,
    CommunityCommentViewSet,
)

router = DefaultRouter()
router.register("query", CommunityQueryViewSet, basename="community_query")
router.register("comment", CommunityCommentViewSet, basename="community_comment")
router.register("queries", CommunityQueryDetailViewSet, basename="community_queries")
router.register(
    "comments", CommunityCommentDetailViewset, basename="community_comments"
)

urlpatterns = [
    path("community/", include(router.urls)),
]
