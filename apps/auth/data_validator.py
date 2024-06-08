from rest_framework import serializers

from apps.user.models import User


class SignupRequestValidator(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password1 = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({"password": "Please enter same password"})

        return attrs


class LoginRequestValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate(self, attrs):
        # for custom data validation
        super().validate(attrs)
        return attrs
