from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
import re

import hashlib

from captain.models import Captain


class CaptainSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Captain
        fields = ['id', 'name', 'surname', 'lastname', 'email', 'phone_number', 'password', 'rate', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_email(self, value):
        if Captain.objects.filter(email=value).exists():
            raise serializers.ValidationError("A captain with that email already exists.")
        return value

    def validate_phone_number(self, value):
        if Captain.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A captain with that phone number already exists.")
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise ValidationError("Invalid phone number format.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        captain = Captain(**validated_data)
        captain.set_password(password)
        captain.save()
        return captain



class CaptainLoginSerializer(serializers.Serializer):
    login = serializers.CharField(
        required=True, 
    )
    password = serializers.CharField(
        required=True, 
    )






# class CaptainTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         if not isinstance(user, Captain):
#             raise AuthenticationFailed('User is not a captain')
#
#         token = super().get_token(user)
#         token['email'] = user.email
#         token['name'] = user.name
#         return token
