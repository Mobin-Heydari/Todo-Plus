from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    # Define the fields to be serialized
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'full_name',
            'password',
            'confirm_password',
            'joined_date',
            'last_login',
            'is_active',
            'is_admin'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'is_verified': {'read_only': True}
        }

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({
                    'password': 'Password fields did not match.'
                })
            if len(data["password"]) <= 8 or len(data["password"]) >= 16:
                raise serializers.ValidationError({
                    'password': 'Password must be between 9 and 15 characters long.'
                })
        elif 'password' in data or 'confirm_password' in data:
            raise serializers.ValidationError({
                'password': 'Both password and confirm_password fields are required.'
            })
        return data

    def update(self, instance, validated_data):
        """
        Update an existing user instance.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()

        return instance