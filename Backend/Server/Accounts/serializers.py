from rest_framework import serializers
from .models import OneTimePassword
from random import randint
import uuid


# Define the OneTimePasswordSerializer class
class OneTimePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for OneTimePassword model.
    Handles creation of new OneTimePassword instances.
    """

    # Define the Meta class to specify the model and fields
    class Meta:
        """
        Meta class for OneTimePasswordSerializer.
        Specifies the model and fields for the serializer.
        """
        # Specify the model for the serializer
        model = OneTimePassword
        # Specify all fields from the model
        exclude = ['code', 'user']


    # Create a new OneTimePassword instance
    def create(self, validated_data):
        """
        Create a new OneTimePassword instance.
        Generates a random 6-digit code and creates a new OneTimePassword instance.
        """
        # Get the request object from the context
        request = self.context.get("request")

        # Generate a random 6-digit code for the OTP
        code = randint(100000, 999999)

        # Create a new OneTimePassword instance with the provided user and generated code
        otp = OneTimePassword.objects.create(
            # Set the user for the OTP
            user=request.user,
            # Set the code for the OTP
            code=code,
            # Generate a UUID for the token
            token=uuid.uuid4()
        )

        # Save the new OneTimePassword instance to the database
        otp.save()

        otp.get_expiration()  # Get the expiration time of the OTP

        # Return the token for the newly created OTP
        return {'token': str(otp.token), 'code': code}



class OneTimePasswordVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying a one-time password.
    """

    # Define the fields for the serializer
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        """
        Validate the incoming data.

        Args:
            attrs (dict): The incoming data.

        Returns:
            dict: The validated data.

        Raises:
            ValidationError: If the data is invalid.
        """
        # Get the token and request from the context
        token = self.context['token']
        request = self.context['request']

        # Try to get the one-time password instance from the database
        try:
            otp = OneTimePassword.objects.get(token=token)
        except OneTimePassword.DoesNotExist:
            # If the one-time password instance does not exist, raise a validation error
            raise serializers.ValidationError({'token': ['Invalid token']})
        
        if not request.user.is_authenticated:
            raise serializers.ValidationError({'unauthorized-user': ['Unauthorized user']})
        if request.user != otp.user:
            raise serializers.ValidationError({'user': ['Invalid user']})
        if otp.status_validation() != 'ACT':
            raise serializers.ValidationError({'expired': ['Expired otp']})
        if int(attrs['code']) != int(otp.code):
            raise serializers.ValidationError({'code': ['Invalid code']})
        
        return attrs
        