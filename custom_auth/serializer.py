from django.contrib.auth import get_user_model
from rest_framework import serializers

from custom_auth.models import Otp

CustomUser = get_user_model()


class CustomAuthSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        otp = Otp.objects.create(user=user)
        otp.send_otp_as_mail()
        return user

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'phone_number', 'email')


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('user', 'code')
