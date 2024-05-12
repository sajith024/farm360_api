from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import (
    CropSeed,
    Fertilizer,
    PestProduct,
)
from .serializers import (
    CropSeedSerializer,
    FertilizerSerializer,
    PestProductSerializer,
)


# Create your views here.
class FertilizerViewSet(ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [IsAuthenticated]


class CropSeedViewSet(ModelViewSet):
    queryset = CropSeed.objects.all()
    serializer_class = CropSeedSerializer
    permission_classes = [IsAuthenticated]


class PestProductViewSet(ModelViewSet):
    queryset = PestProduct.objects.all()
    serializer_class = PestProductSerializer
    permission_classes = [IsAuthenticated]
