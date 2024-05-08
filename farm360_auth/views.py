import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth import authenticate
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from .models import Farm360User, Farm360UserProfile, Role, Country, Language
from .serializers import (
    RegistrationUserSerializer,
    LoginUserSerializer,
    RoleSerializer,
    CountrySerializer,
    LanguageSerializer,
    UserProfileSerializer,
    UserProfileListSerializer,
)
from .pagination import UserPagination


logger = logging.getLogger(__name__)


@extend_schema_view()
class RegistrationUserView(CreateAPIView):
    queryset = Farm360User.objects.all()
    serializer_class = RegistrationUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            token = RefreshToken.for_user(user=serializer.instance)
            data = {
                "data": {
                    "id": serializer.instance.id,
                    "first_name": serializer.instance.first_name,
                    "token": {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    },
                },
                "message": "Registration successful",
            }
            return Response(data, status=HTTP_201_CREATED)
        else:
            return Response(
                {"errors": serializer.errors, "message": "Registration failed"},
                status=HTTP_400_BAD_REQUEST,
            )


@extend_schema_view()
class LoginUserView(CreateAPIView):
    serializer_class = LoginUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                token = RefreshToken.for_user(user)
                data = {
                    "message": "Login successful",
                    "data": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "token": {
                            "refresh": str(token),
                            "access": str(token.access_token),
                        },
                    },
                }
                logger.info(f"Login successful for {user.email}")
                return Response(data, status=HTTP_200_OK)
            else:
                logger.warning("Unauthorized Login.")
                return Response(data=serializer.errors, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema_view()
class LogoutUserView(TokenBlacklistView):
    pass


@extend_schema_view()
class RolesViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class CountryView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class LanguageView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view()
class UserViewSet(ModelViewSet):
    queryset = Farm360UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserProfileListSerializer

        return super().get_serializer_class()
