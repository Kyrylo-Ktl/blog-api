"""Module for describing serialization of models"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Model serializer for User class"""

    email = serializers.EmailField(validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    username = serializers.CharField(min_length=4, max_length=32,
                                     validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    first_name = serializers.CharField(min_length=2, max_length=64, required=False)
    last_name = serializers.CharField(min_length=2, max_length=64, required=False)
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
