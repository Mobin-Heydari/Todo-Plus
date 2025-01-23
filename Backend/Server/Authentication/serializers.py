from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.tokens import TokenError

from Users.models import User


class TokenObtainSerializer(TokenObtainPairSerializer):
    # Custom Token Obtain Serializer that inherits from TokenObtainPairSerializer
    
    @classmethod
    def get_token(cls, user):
        # Override the get_token method to add custom claims to the token
        
        # Call the parent class's get_token method to get the default token
        token = super().get_token(user)
        
        # Add custom claims to the token
        # User custom claims
        token['username'] = user.username  # Add the user's username to the token
        token['email'] = user.email  # Add the user's email to the token
        token['joined_date'] = str(user.joined_date)  # Add the user's joined date to the token
        
        # User profiles claims
        token['full_name'] = user.full_name  # Add the user's full name to the token
        
        # Return the token with the added custom claims
        return token
    

# Define the LoginSerializer class
class LoginSerializer(serializers.Serializer):
    """
    Serializer to validate email and password.
    """
    # Define the email field
    email = serializers.CharField(max_length=255)
    
    # Define the password field
    password = serializers.CharField(max_length=255, write_only=True)

    # Validate the email field
    def validate_email(self, value):
        # Check if the email exists in the database
        if not User.objects.filter(email=value).exists():
            # Raise a validation error if the email does not exist
            raise serializers.ValidationError('email does not exist')
        # Return the validated email
        return value

    # Validate the password field
    def validate_password(self, value):
        # Check if the password is at least 8 characters long
        if len(value) < 8:
            # Raise a validation error if the password is too short
            raise serializers.ValidationError('Password must be at least 8 characters long')
        # Return the validated password
        return value

    # Validate the entire serializer
    def validate(self, data):
        # Get the email and password from the data
        email = data.get('email')
        password = data.get('password')
        
        # Check if both email and password are provided
        if email is None or password is None:
            # Raise a validation error if either email or password is missing
            raise serializers.ValidationError('Both email and password are required')
        
        # Get the user object from the database
        user = User.objects.get(email=email)
        
        # Check if the password is correct
        if not user.check_password(password):
            # Raise a validation error if the password is incorrect
            raise serializers.ValidationError('Invalid password')
        
        # Return the validated data
        return data
    
# Create a serializer to validate logout requests
class LogoutSerializer(serializers.Serializer):
    """
    Serializer to validate logout requests.
    
    This serializer validates the refresh token and returns a success response.
    """
    # Define the refresh token field
    refresh_token = serializers.CharField(max_length=255)
    
    # Define the permission classes for the serializer
    # permission_classes = [IsTokenOwnerOrStaff]  # Not recommended
    
    # Define the validate method to validate the data
    def validate(self, data):
        """
        Validate the data.
        
        This method checks if the refresh token is valid and if the user has permission to revoke it.
        """
        # Get the refresh token from the data
        refresh_token = data.get('refresh_token')
        
        # Check if the refresh token is provided
        if not refresh_token:
            # If the refresh token is not provided, raise a validation error
            raise serializers.ValidationError('Refresh token is required')
        
        # Try to get the token object from the refresh token
        try:
            token = RefreshToken(refresh_token)
        except Exception as e:
            # If the token is invalid, raise a validation error
            raise serializers.ValidationError('Invalid refresh token')
        
        # Get the user ID from the token payload
        user_id = token.payload.get('user_id')
        
        # Get the user instance from the database
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # If the user does not exist, raise a validation error
            raise serializers.ValidationError('User does not exist')
        
        # Check if the user is the owner of the token or a staff user
        if self.context['request'].user != user and not self.context['request'].user.is_staff:
            # If the user is not the owner of the token or a staff user, raise a validation error
            raise serializers.ValidationError('You do not have permission to revoke this token')
        
        # Return the validated data
        return data