from django.utils import timezone
from django.contrib.auth import get_user_model

from django.db.models import Model
from django.db.models import CharField, TextField, FileField, DateTimeField
from django.db.models import ForeignKey, ManyToManyField, CASCADE


# Create your models here.
class FertilizerProvider(Model):
    name = CharField(max_length=150)
    phone_number = CharField(max_length=15, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class CropSeedProvider(Model):
    name = CharField(max_length=150)
    phone_number = CharField(max_length=15, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Fertilizer(Model):
    name = CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class CropSeed(Model):
    name = CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Crop(Model):
    name = CharField(max_length=150)
    description = TextField(max_length=1000, blank=True, default="")
    user = ForeignKey(get_user_model(), on_delete=CASCADE, related_name="crops")
    fertilizer = ManyToManyField(Fertilizer, related_name="crops")
    crop_seed = ManyToManyField(CropSeed, related_name="crops")
    fertilizer_provider = ForeignKey(
        FertilizerProvider, on_delete=CASCADE, related_name="crops"
    )
    crop_seed_provider = ForeignKey(
        CropSeedProvider, on_delete=CASCADE, related_name="crops"
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class CropStage(Model):
    CROP_STAGES = (
        ("seeding", "Seeding Stage"),
        ("vegetative", "Vegetative Stage"),
        ("flowering", "Flowering Stage"),
        ("fruiting", "Fruiting Stage"),
        ("harvest", "Harvesting Stage"),
    )
    crop = ForeignKey(Crop, on_delete=CASCADE, related_name="crop_stages")
    stage = CharField(choices=CROP_STAGES, default="seeding")
    video = FileField(upload_to="crop/stage/video", default="", blank=True)
    title = CharField(max_length=200, default="", blank=True)
    description = TextField(max_length=1000, blank=True, default="")

    def __str__(self) -> str:
        return self.stage


class PestProduct(Model):
    name = CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class CropPestDisease(Model):
    crop = ForeignKey(Crop, on_delete=CASCADE, related_name="pest_diseases")
    insect_name = CharField(max_length=150)
    symptoms = TextField(max_length=500, blank=True, default="")
    pest_product = ManyToManyField(PestProduct, related_name="pest_diseases")
