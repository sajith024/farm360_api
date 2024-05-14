from django.db import transaction
from rest_framework.serializers import ModelSerializer

from .models import (
    Crop,
    CropPestDisease,
    CropSeed,
    CropSeedProvider,
    CropStage,
    Fertilizer,
    FertilizerProvider,
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


class CropStageSerializer(ModelSerializer):
    class Meta:
        model = CropStage
        fields = "__all__"


class FertilizerProviderSerializer(ModelSerializer):
    class Meta:
        model = FertilizerProvider
        fields = "__all__"


class CropSeedProviderSerializer(ModelSerializer):
    class Meta:
        model = CropSeedProvider
        fields = "__all__"


class CropPestDiseaseSerializer(ModelSerializer):
    class Meta:
        model = CropPestDisease
        fields = (
            "id",
            "insect_name",
            "symptoms",
            "pest_product",
            "chemical_control",
            "biological_control",
        )


class CropSerializer(ModelSerializer):
    fertilizer_provider = FertilizerProviderSerializer()
    crop_seed_provider = CropSeedProviderSerializer()
    pest_diseases = CropPestDiseaseSerializer(many=True)

    class Meta:
        model = Crop
        fields = (
            "id",
            "name",
            "description",
            "fertilizers",
            "fertilizer_provider",
            "crop_seeds",
            "crop_seed_provider",
            "pest_diseases",
        )

    def create(self, validated_data):
        request = self.context["request"]
        pest_diseases_data = validated_data.pop("pest_diseases")
        fertilizers = validated_data.pop("fertilizers")
        crop_seeds = validated_data.pop("crop_seeds")
        fertilizer_prov_data = validated_data.pop("fertilizer_provider")
        cropseed_prov_data = validated_data.pop("crop_seed_provider")

        fertilizer_prov = FertilizerProvider.objects.get_or_create(
            **fertilizer_prov_data
        )[0]
        cropseed_prov = CropSeedProvider.objects.get_or_create(**cropseed_prov_data)[0]

        with transaction.atomic():
            crop = Crop.objects.create(
                **validated_data,
                user=request.user,
                fertilizer_provider=fertilizer_prov,
                crop_seed_provider=cropseed_prov,
            )

            for fertilizer in fertilizers:
                crop.fertilizers.add(fertilizer)

            for crop_seed in crop_seeds:
                crop.crop_seeds.add(crop_seed)

            for pest_disease in pest_diseases_data:
                pest_products = pest_disease.pop("pest_product")
                crop_pest = CropPestDisease.objects.create(**pest_disease, crop=crop)
                for product in pest_products:
                    crop_pest.pest_product.add(product)

        return crop


class CropImageSerializer(ModelSerializer):
    class Meta:
        model = Crop
        fields = ("image",)

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance
