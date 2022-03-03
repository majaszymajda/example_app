from django.contrib.auth import authenticate, password_validation
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_active", "first_name", "last_name")


class UserPasswordUpdateSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    default_error_messages = {"invalid_password": _("Podano nie właściwe hasło.")}

    def validate_old_password(self, value):
        user = self.context.get("view").get_object()
        if not user.check_password(value):
            self.fail("invalid_password")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": _("Podane hasła nie są zgodne.")}
            )
        password_validation.validate_password(
            data["new_password"], self.context["request"].user
        )
        return data

    def update(self, instance, validated_data):

        instance.update_password(validated_data["new_password"])
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            _("Unable to log in with provided credentials.")
        )

    def create(self, instance):
        token = instance.create_token()
        return token

