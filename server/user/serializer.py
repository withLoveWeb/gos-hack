from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re


UserProfile = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'second_name', 'last_name', 'email', 'phone_number', 'birth_date', 'password')

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def validate_phone_number(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise ValidationError("Invalid phone number format.")
        return value

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['email'],  
            first_name=validated_data['first_name'],
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date', None),
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
        return user
