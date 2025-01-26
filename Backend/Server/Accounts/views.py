from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from Users.models import User
from .models import OneTimePassword
from .serializers import OneTimePasswordSerializer, OneTimePasswordVerificationSerializer



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

class AccountVerificationView(APIView):
    """
    View for verifying a one-time password.
    """

    def post(self, request, token):
        """
        Handle POST requests to verify a one-time password.

        Args:
            request (Request): The incoming request.
            token (str): The token to verify.

        Returns:
            Response: A response with the verification result.
        """
        # Create a serializer instance with the incoming data and context
        serializer = OneTimePasswordVerificationSerializer(data=request.data, context={'token': token, 'request': request})

        # Check if the serializer is valid
        if serializer.is_valid():
            # Changing the user is_verified to True value and save it
            user = request.user
            user.is_verified = True
            user.save()
            # If the serializer is valid, return a success response
            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        else:
            # If the serializer is not valid, get the error messages
            errors = serializer.errors

            # Map the error messages to specific status codes
            if 'unauthorized-user' in errors:
                # Return a 401 UNAUTHORIZED response
                return Response({'errors': errors}, status=status.HTTP_401_UNAUTHORIZED)
            elif 'user' in errors:
                # Return a 403 FORBIDDEN response
                return Response({'errors': errors}, status=status.HTTP_403_FORBIDDEN)
            else:
                # Return a 400 BAD REQUEST response
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)