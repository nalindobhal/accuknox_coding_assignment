from django.db import transaction
from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['username'] = validated_data.get('email').split("@")[0]
        with transaction.atomic():
            instance: User = super().create(validated_data)
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
