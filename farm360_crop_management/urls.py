from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FertilizerViewSet,
    CropSeedViewSet,
    PestProductViewSet,
    CropListView,
    CropDetailView,
    CropViewSet,
    CropImageView,
    CropStagesViewSet,
)

router = DefaultRouter()
router.register("fertilizers", FertilizerViewSet, basename="crop_fertilizers")
router.register("seeds", CropSeedViewSet, basename="crop_seeds")
router.register("pesticide", PestProductViewSet, basename="crop_pesticide")
router.register("crop/stages", CropStagesViewSet, basename="crop_stages")
router.register("crop", CropViewSet, basename="crop_crop")

urlpatterns = [
    path("crops/", CropListView.as_view(), name="crops"),
    path("crops/crop/<int:pk>/image/", CropImageView.as_view(), name="crop_image"),
    path("crops/crop/detail/<int:pk>", CropDetailView.as_view(), name="crop_detail"),
    path("crops/", include(router.urls)),
]
