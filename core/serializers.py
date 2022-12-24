from django import forms
from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.hashers import make_password

USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])
    password_repeat = serializers.CharField(write_only=True)

    def create(self, validated_data) -> USER_MODEL:
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Пароли не совпадают.')

        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        result = super().create(validated_data)
        return result

    class Meta:
        model = USER_MODEL
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat",)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ('username', 'password', )

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'],
                            password=validated_data['password'],
                            )
        if not user:
            raise exceptions.AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = data['user']
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'old_password': 'incorrect password'})
        return data

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
