from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from Users.models import User
from .models import OneTimePassword
from .serializers import OneTimePasswordSerializer



# Define the GenerateOTPView class
class GenerateOTPView(APIView):
    """
    View for generating a One-Time Password (OTP) for user verification.
    Handles POST requests to generate a new OTP.
    """

    # Handle POST requests to generate a new OTP
    def get(self, request):
        """
        Handle POST requests to generate a new OTP.
        Validates the incoming data and generates a new OTP if valid.
        """
        # Create a new OneTimePasswordSerializer instance with the incoming data
        serializer = OneTimePasswordSerializer(data=request.data, context={'request': request})

        # Check if the incoming data is valid
        if serializer.is_valid(raise_exception=True):
            # Create a new OTP instance using the validated data
            otp_data = serializer.create(serializer.validated_data)

            # Return a successful response with the OTP token
            return Response(
                {
                    # Message indicating that the OTP was sent successfully
                    'message': 'OTP sent successfully',
                    # Token for the newly generated OTP
                    'otp': otp_data
                },
                # HTTP status code for created resources
                status=status.HTTP_201_CREATED
            )
        else:
            # Return an error response with validation errors
            return Response(
                # Validation errors from the serializer
                serializer.errors,
                # HTTP status code for bad requests
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Define a method to handle exceptions raised during view execution
    def handle_exception(self, exc):
        """
        Handle exceptions raised during view execution.
        
        :param exc: The exception object
        :return: A response object with an error message
        """
        
        # Check if the exception is a validation error
        if isinstance(exc, ValidationError):
            # Return a response with the validation errors
            return Response({'error': 'Validation error', 'details': exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        # Call the parent class's handle_exception method for other exceptions
        return super().handle_exception(exc)