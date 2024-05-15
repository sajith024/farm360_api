import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ImageField,
    ModelSerializer,
    Serializer,
)

from farm360_auth.models import (
    Country,
    Farm360User,
    Farm360UserProfile,
    Language,
    PhoneCode,
    Role,
)


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z ]{1,97}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value

    def validate_code(self, value):
        if not re.match(r"^\d{3}$", value):
            raise ValidationError("Code must be 3 digits")
        return value

    def validate_flag(self, value):
        max_size = 1024**2
        if value.size > max_size:
            raise ValidationError("Image size should not exceed 1MB.")
        return value


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z ]{1,147}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"

    def validate_name(self, value):
        if not re.match(r"^[a-zA-Z][a-zA-Z ]{1,97}[a-zA-Z]$", value):
            raise ValidationError(
                "Name must contain space, hyphen, only alphabetic characters by start and end."
            )
        return value


class PhoneCodeSerializer(ModelSerializer):
    flag = ImageField(source="country.flag")

    class Meta:
        model = PhoneCode
        fields = (
            "id",
            "flag",
            "code",
        )

    def validate_code(self, value):
        if not re.match(r"^\d{3}$", value):
            raise ValidationError("Code must be 3 digits")
        return value


class RegistrationUserSerializer(ModelSerializer):
    class Meta:
        model = Farm360User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def validate_email(self, value):
        if not re.match(r"^[\w\-\.]+@[\w-]+\.[^\d\s-]{2,4}$", value):
            raise ValidationError("Code must be 3 digits")
        return value

    def validate_first_name(self, value):
        if not re.match(r"^[A-Z][a-z]{,147}[^\s\d]$", value):
            raise ValidationError("Enter valid name.")
        return value

    def validate_last_name(self, value):
        if not re.match(r"^[A-Z][a-z]{,147}[^\s\d]$", value):
            raise ValidationError("Enter valid name.")
        return value

    def validate_password(self, value):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value
        ):
            raise ValidationError(
                "Minimum eight characters, at least one letter, one number and one special character"
            )
        return value

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

    def validate_image(self, value):
        max_size = 5 * (1024**2)
        if value.size > max_size:
            raise ValidationError("Image size should not exceed 5MB.")
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^[6-9]\d{9}$", value):
            raise ValidationError("Enter valid phone number")
        return value

    def create(self, validated_data):
        user_serializer = RegistrationUserSerializer(data=validated_data.pop("user"))
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        role = Role.objects.get_or_create(name="User")[0]
        profile = Farm360UserProfile.objects.create(
            **validated_data, user=user, role=role
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
