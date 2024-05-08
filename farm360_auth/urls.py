from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegistrationUserView,
    LoginUserView,
    LogoutUserView,
    RolesViewSet,
    CountryView,
    LanguageView,
    UserViewSet,
)

router = DefaultRouter()
router.register("roles", RolesViewSet, basename="role")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("signup/", RegistrationUserView.as_view(), name="api_signup"),
    path("login/", LoginUserView.as_view(), name="api_login"),
    path("logout/", LogoutUserView.as_view(), name="api_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("countries/", CountryView.as_view(), name="countries"),
    path("languages/", LanguageView.as_view(), name="languages"),
    path("", include(router.urls)),
]
