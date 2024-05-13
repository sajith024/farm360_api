import logging

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import (
    Crop,
    CropSeed,
    Fertilizer,
    PestProduct,
)
from .serializers import (
    CropSerializer,
    CropImageSerializer,
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
class CropImageView(UpdateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropImageSerializer
    permission_classes = [IsAuthenticated]
