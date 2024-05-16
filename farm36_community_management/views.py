import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from farm360_auth.pagination import UserPagination

logger = logging.getLogger(__name__)

from .models import (
    CommunityQuery,
    CommunityComment,
    CommunityQueryImage,
    CommunityCommentImage,
)

from .serializers import (
    CommunityQueryDetailSerializer,
    CommunityQueryCommentDetailSerializer,
    CommunityQuerySerializer,
    CommunityCommentSerializer,
)


# Create your views here.
@extend_schema_view()
class CommunityQueryDetailList(ListAPIView):
    queryset = CommunityQuery.objects.all()
    serializer_class = CommunityQueryDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination


@extend_schema_view()
class CommunityCommentDetailList(ListAPIView):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityQueryCommentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_id = self.request.query_params.get("query")
        if query_id:
            return self.queryset.filter(query_id=query_id, main=None)

        return self.queryset.filter(main=None)


@extend_schema_view()
class CommunityQueryViewSet(ModelViewSet):
    queryset = CommunityQuery.objects.all()
    serializer_class = CommunityQuerySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema_view()
class CommunityCommentViewSet(ModelViewSet):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
