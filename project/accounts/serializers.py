"""Module for describing serialization of models"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import BooleanField, CharField, EmailField, ModelSerializer
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    """Model serializer for User class"""

    email = EmailField(validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    username = CharField(min_length=4, max_length=32,
                         validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    first_name = CharField(min_length=2, max_length=64, required=False, allow_blank=True)
    last_name = CharField(min_length=2, max_length=64, required=False, allow_blank=True)
    password = CharField(min_length=8, max_length=64, write_only=True)
    is_superuser = BooleanField(read_only=True)
    is_staff = BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
            instance.save()
        return super(UserSerializer, self).update(instance, validated_data)
