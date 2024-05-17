from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CountryView,
    DashboardStatsView,
    LanguageView,
    LoginUserView,
    LogoutUserView,
    PhoneCodeView,
    RegistrationUserView,
    RolesViewSet,
    UserProfileViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("roles", RolesViewSet, basename="role")
router.register("users/profile", UserProfileViewSet, basename="users_profile")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("signup/", RegistrationUserView.as_view(), name="api_signup"),
    path("login/", LoginUserView.as_view(), name="api_login"),
    path("logout/", LogoutUserView.as_view(), name="api_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard_stats"),
    path("countries/", CountryView.as_view(), name="countries"),
    path("phonecodes/", PhoneCodeView.as_view(), name="phone_codes"),
    path("languages/", LanguageView.as_view(), name="languages"),
    path("", include(router.urls)),
]
