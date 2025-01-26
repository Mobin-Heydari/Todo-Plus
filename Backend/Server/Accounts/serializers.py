from rest_framework import serializers

from .models import OneTimePassword

from random import randint
import uuid




# Define the OneTimePasswordSerializer class
class OneTimePasswordSerializer(serializers.ModelSerializer):
    # Define the Meta class to specify the model and fields
    class Meta:
        # Specify the model for the serializer
        model = OneTimePassword
        # Specify all fields from the model
        fields = "__all__"

    # Define the create method to create a new OneTimePassword instance
    def create(self, validated_data):
        # Generate a random 6-digit code for the OTP
        code = randint(100000, 999999)
        
        # Create a new OneTimePassword instance with the provided user and generated code
        otp = OneTimePassword.objects.create(
            # Set the user for the OTP
            user=validated_data['user'],
            # Set the code for the OTP
            code=code,
            # Generate a UUID for the token
            token=uuid.uuid4()
        )

        # Save the new OneTimePassword instance to the database
        otp.save()

        # Return the token for the newly created OTP
        return {'token': str(otp.token)}