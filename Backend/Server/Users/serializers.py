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
            'id',
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
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        """
        Validate the password and confirm password fields.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'password': 'Password fields did not match.'
            })
        if len(data["password"]) <= 8 or len(data["password"]) >= 16:
            raise serializers.ValidationError({
                'password': 'Password must be between 9 and 15 characters long.'
            })
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user instance.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance