from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.serializers import CharField, ImageField

from farm360_auth.models import (
    Farm360User,
    Farm360UserProfile,
    Role,
    Country,
    Language,
    PhoneCode,
)


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class PhoneCodeSerializer(ModelSerializer):
    flag = ImageField(source="country.flag")

    class Meta:
        model = PhoneCode
        fields = (
            "id",
            "flag",
            "code",
        )


class RegistrationUserSerializer(ModelSerializer):
    class Meta:
        model = Farm360User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        user = Farm360User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class UserProfileListSerializer(ModelSerializer):
    email = CharField(source="user.email")
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    role = CharField(source="role.name")
    language = CharField(source="language.name")
    country = CharField(source="country.name")

    class Meta:
        model = Farm360UserProfile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "phone_number",
            "role",
            "language",
            "country",
        )


class UserProfileSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name", required=False)
    email = CharField(source="user.email")
    password = CharField(source="user.password", write_only=True)

    class Meta:
        model = Farm360UserProfile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "image",
            "phone_code",
            "phone_number",
            "language",
            "country",
        )
        read_only_fields = ("role",)

    def create(self, validated_data):
        user_serializer = RegistrationUserSerializer(data=validated_data.pop("user"))
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        role = Role.objects.get_or_create(name="User")
        profile = Farm360UserProfile.objects.create(
            **validated_data, user=user, role=role[0]
        )
        profile.save()
        return profile

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            user_data = validated_data.pop("user")
            instance.user.first_name = user_data.get(
                "first_name", instance.user.first_name
            )
            instance.user.last_name = user_data.get(
                "last_name", instance.user.last_name
            )
            instance.user.save()

        instance.phone_code = validated_data.get("phone_code", instance.phone_code)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.role = validated_data.get("role", instance.role)
        instance.language = validated_data.get("language", instance.language)
        instance.country = validated_data.get("country", instance.country)
        instance.image = validated_data.get("image", instance.image)

        instance.save()

        return instance


class LoginUserSerializer(Serializer):
    email = CharField()
    password = CharField()
