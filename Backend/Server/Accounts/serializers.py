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

    # Validate the incoming data
    def validate(self, attrs):
        """
        Validate the incoming data.
        Checks if the user is authenticated, active, and not already verified.
        """
        # Get the request object from the context
        request = self.context.get("request")

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")
        # Check if the user is active
        if not request.user.is_active:
            raise serializers.ValidationError("User is not active")
        # Check if the user is already verified
        if request.user.is_verified:
            raise serializers.ValidationError("User is already verified")
        
        return attrs

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

        # Return the token for the newly created OTP
        return {'token': str(otp.token)}