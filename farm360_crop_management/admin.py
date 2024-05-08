from django.contrib import admin

from .models import (
    FertilizerProvider,
    CropSeedProvider,
    Fertilizer,
    CropSeed,
    Crop,
    CropStage,
    PestProduct,
    CropPestDisease,
)

# Register your models here.
admin.site.register(
    (
        FertilizerProvider,
        CropSeedProvider,
        Fertilizer,
        CropSeed,
        Crop,
        CropStage,
        PestProduct,
        CropPestDisease,
    )
)
