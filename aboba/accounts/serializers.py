from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(
            **validated_data,
            password=password,
        )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {
            'refresh': str(refresh),
            'access': access_token,
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        if not refresh_token:
            raise serializers.ValidationError('Refresh token is required')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise serializers.ValidationError(f'Token error: {str(e)}')
        return {'message': 'Logout successful!'}


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        if not refresh_token:
            raise serializers.ValidationError('Refresh token is required')
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)
        except TokenError as e:
            raise serializers.ValidationError(f'Token error: {str(e)}')
        return {
            'access': access_token,
            'refresh': new_refresh_token,
        }
