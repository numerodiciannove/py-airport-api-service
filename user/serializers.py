from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, generics


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "is_staff",
            "user_image"
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email,
                                password=password,
                                )
            if not user:
                raise serializers.ValidationError(
                    _("Unable to log in with provided credentials.")
                )
        else:
            raise serializers.ValidationError(
                _("Must include 'email' and 'password'.")
            )
        attrs["user"] = user
        return attrs
