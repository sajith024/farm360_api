import re

from django.db import transaction
from rest_framework.exceptions import ValidationError
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

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,197}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate(self, data):
        name = data.get("name")
        if name:
            existing_instance = Fertilizer.objects.filter(name=name).first()
            if existing_instance:
                raise ValidationError("This name already exists.")
        return data


class CropSeedSerializer(ModelSerializer):
    class Meta:
        model = CropSeed
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,197}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate(self, data):
        name = data.get("name")
        if name:
            existing_instance = CropSeed.objects.filter(name=name).first()
            if existing_instance:
                raise ValidationError("This name already exists.")
        return data


class PestProductSerializer(ModelSerializer):
    class Meta:
        model = PestProduct
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,147}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate(self, data):
        name = data.get("name")
        if name:
            existing_instance = PestProduct.objects.filter(name=name).first()
            if existing_instance:
                raise ValidationError("This name already exists.")
        return data


class CropStageSerializer(ModelSerializer):
    class Meta:
        model = CropStage
        fields = "__all__"

    def validate_title(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{10,197}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_description(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9.,!?\-;:()\'\"\s]{10,999}$", value):
            raise ValidationError("Description contains invalid characters.")

        return value

    def validate_video(self, value):
        max_size = 20 * (1024**2)

        if value.size > max_size:
            raise ValidationError("Image size should not exceed 20MB.")
        return value


class FertilizerProviderSerializer(ModelSerializer):
    class Meta:
        model = FertilizerProvider
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,147}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^\d{6,14}$", value):
            raise ValidationError("Invalid contact number format.")

        return value


class CropSeedProviderSerializer(ModelSerializer):
    class Meta:
        model = CropSeedProvider
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,97}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^\d{6,15}$", value):
            raise ValidationError("Invalid contact number format.")

        return value


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

    def validate_insect_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,147}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_symptoms(self, value):
        if not re.match(r"^[a-zA-Z][[a-zA-Z0-9.,!?;:()\-\'\"\s]{10,499}$", value):
            raise ValidationError(
                "Symptoms contains invalid characters, should be 50 - 500 characters."
            )

        return value

    def validate_chemical_control(self, value):
        if value and not re.match(
            r"^[a-zA-Z][a-zA-Z0-9.,!?\-;:()\'\"\s]{10,999}$", value
        ):
            raise ValidationError(
                "Chemical Control contains invalid characters, should be 50 - 1000 characters."
            )

        return value

    def validate_biological_control(self, value):
        if value and not re.match(
            r"^[a-zA-Z][a-zA-Z0-9.,!?\-;:()\'\"\s]{10,999}$", value
        ):
            raise ValidationError(
                "Biological Control contains invalid characters, should be 50 - 1000 characters."
            )

        return value


class CropListSerializer(ModelSerializer):
    class Meta:
        model = Crop
        fields = (
            "id",
            "name",
            "description",
            "image",
            "created_at",
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

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z -]{1,147}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_description(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9.,!?\-;:()\'\"\s]{10,999}$", value):
            raise ValidationError("Description contains invalid characters.")

        return value

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

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)

        fertilizer_provider = validated_data.get("fertilizer_provider")
        if fertilizer_provider:
            fertilizer_prov = FertilizerProvider.objects.get_or_create(
                **fertilizer_provider
            )[0]
            instance.fertilizer_provider = fertilizer_prov

        crop_seed_provider = validated_data.get("crop_seed_provider")
        if crop_seed_provider:
            cropseed_prov = CropSeedProvider.objects.get_or_create(
                **crop_seed_provider
            )[0]
            instance.crop_seed_provider = cropseed_prov

        instance.save()

        fertilizers = validated_data.get("fertilizers")
        if fertilizers:
            instance.fertilizers.clear()
            for fertilizer in fertilizers:
                instance.fertilizers.add(fertilizer)

        crop_seeds = validated_data.get("crop_seeds")
        if crop_seeds:
            instance.crop_seeds.clear()
            for crop_seed in crop_seeds:
                instance.crop_seeds.add(crop_seed)

        pest_diseases = validated_data.get("pest_diseases")
        if pest_diseases:
            for pest_disease in instance.pest_diseases.all():
                pest_disease.delete()

            for pest_disease in pest_diseases:
                pest_products = pest_disease.pop("pest_product")
                crop_pest = CropPestDisease.objects.create(
                    **pest_disease, crop=instance
                )
                for product in pest_products:
                    crop_pest.pest_product.add(product)

        return instance


class CropImageSerializer(ModelSerializer):
    class Meta:
        model = Crop
        fields = ("image",)

    def validate_image(self, value):
        max_size = 5 * (1024**2)
        if value.size > max_size:
            raise ValidationError("Image size should not exceed 5MB.")
        return value

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance


class CropPestDetailDiseaseSerializer(ModelSerializer):
    pest_product = PestProductSerializer(many=True)

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


class CropDetailSerializer(ModelSerializer):
    fertilizer_provider = FertilizerProviderSerializer()
    crop_seed_provider = CropSeedProviderSerializer()
    pest_diseases = CropPestDetailDiseaseSerializer(many=True)
    crop_stages = CropStageSerializer(many=True)
    fertilizers = FertilizerSerializer(many=True)
    crop_seeds = CropSeedSerializer(many=True)

    class Meta:
        model = Crop
        fields = (
            "id",
            "name",
            "image",
            "description",
            "crop_stages",
            "fertilizers",
            "fertilizer_provider",
            "crop_seeds",
            "crop_seed_provider",
            "pest_diseases",
        )
