import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.viewsets import ModelViewSet

from farm360_auth.pagination import UserPagination

from .models import (
    Crop,
    CropSeed,
    CropStage,
    Fertilizer,
    PestProduct,
)
from .serializers import (
    CropSerializer,
    CropListSerializer,
    CropDetailSerializer,
    CropImageSerializer,
    CropStageSerializer,
    CropSeedSerializer,
    FertilizerSerializer,
    PestProductSerializer,
)

logger = logging.getLogger(__name__)


# Create your views here.
@extend_schema_view()
class FertilizerViewSet(ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CropSeedViewSet(ModelViewSet):
    queryset = CropSeed.objects.all()
    serializer_class = CropSeedSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class PestProductViewSet(ModelViewSet):
    queryset = PestProduct.objects.all()
    serializer_class = PestProductSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CropViewSet(ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CropListView(ListAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "created_at"]
    ordering_fields = ["name", "created_at"]


@extend_schema_view()
class CropDetailView(RetrieveAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropDetailSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CropImageView(UpdateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropImageSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CropStagesViewSet(ModelViewSet):
    queryset = CropStage.objects.all()
    serializer_class = CropStageSerializer
    permission_classes = [IsAuthenticated]
