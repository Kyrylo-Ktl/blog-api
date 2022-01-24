"""Module for describing serialization of models"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import BooleanField, CharField, EmailField, ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserDetailsSerializer(ModelSerializer):
    """Model serializer for retrieving user details"""

    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = CharField(min_length=4, max_length=32,
                         validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = CharField(min_length=2, max_length=64)
    last_name = CharField(min_length=2, max_length=64)
    is_superuser = BooleanField(read_only=True)
    is_staff = BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff',)


class UserCreateSerializer(UserDetailsSerializer):
    """Model serializer for creating user"""

    password = CharField(min_length=8, max_length=64, write_only=True,
                         validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data.pop('password')
        return super(UserCreateSerializer, self).update(instance, validated_data)


class ResetPasswordEmailRequestSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {'email': {'required': True}}

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError('No user with such email.')
        return value


class ResetPasswordConfirmSerializer(ModelSerializer):
    password = CharField(min_length=8, max_length=64, required=True,
                         validators=[validate_password])

    class Meta:
        model = User
        fields = ('password',)
