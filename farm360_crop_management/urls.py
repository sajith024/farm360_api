from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FertilizerViewSet,
    CropSeedViewSet,
    PestProductViewSet,
)

router = DefaultRouter()
router.register("fertilizers", FertilizerViewSet, basename="crop_fertilizers")
router.register("seeds", CropSeedViewSet, basename="crop_seeds")
router.register("pesticide", PestProductViewSet, basename="crop_pesticide")

urlpatterns = [path("crop/", include(router.urls))]
