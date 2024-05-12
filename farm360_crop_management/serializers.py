from rest_framework.serializers import ModelSerializer

from .models import (
    CropSeed,
    Fertilizer,
    PestProduct,
)


class FertilizerSerializer(ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = "__all__"


class CropSeedSerializer(ModelSerializer):
    class Meta:
        model = CropSeed
        fields = "__all__"


class PestProductSerializer(ModelSerializer):
    class Meta:
        model = PestProduct
        fields = "__all__"
