from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CommunityQueryDetailList,
    CommunityCommentDetailList,
    CommunityQueryViewSet,
    CommunityCommentViewSet,
)

router = DefaultRouter()
router.register("query", CommunityQueryViewSet, basename="community_query")
router.register("comment", CommunityCommentViewSet, basename="community_comment")

urlpatterns = [
    path(
        "community/queries/",
        CommunityQueryDetailList.as_view(),
        name="community_queries",
    ),
    path(
        "community/comments/",
        CommunityCommentDetailList.as_view(),
        name="community_comments",
    ),
    path("community/", include(router.urls)),
]
