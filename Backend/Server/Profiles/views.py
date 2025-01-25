from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer

from Users.models import User



class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Profile model.
    """
    # Define the queryset for the viewset
    queryset = Profile.objects.all()
    # Define the serializer class for the viewset
    serializer_class = ProfileSerializer
    # Define the permission classes for the viewset
    permission_classes = [IsAuthenticated]
    # Defines the required field for retrieve methods
    lookup_field = 'user_username'

    # Define the list method for the viewset
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve a list of profiles.
        """
        try:
            # Check if the user is staff
            if request.user.is_staff:
                # Retrieve the queryset
                queryset = Profile.objects.all()
                # Serialize the queryset
                serializer = self.serializer_class(queryset, many=True)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the retrieve method for the viewset
    def retrieve(self, request, user_username, *args, **kwargs):
        """
        Handle GET requests to retrieve a single profile.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.is_staff or request.user.username == user_username:
                # Getting the user instance
                instance = get_object_or_404(User, username=user_username)
                # Retrieve the profile instance
                queryset = get_object_or_404(Profile, user=instance)
                # Serialize the profile instance
                serializer = self.serializer_class(queryset)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except Profile.DoesNotExist:
            # Return a 404 Not Found response if the profile does not exist
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the update method for the viewset
    def update(self, request, user_username, *args, **kwargs):
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == user_username or request.user.is_staff:
                # Getting the user instance
                instance = get_object_or_404(User, username=user_username)
                # Retrieve the profile instance
                queryset = get_object_or_404(Profile, user=instance)
                # Serialize the profile instance
                serializer = self.serializer_class(queryset, data=request.data, partial=True)
                # Validate the serializer
                serializer.is_valid(raise_exception=True)
                # Update the profile instance
                serializer.save()
                # Return the serialized data
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to update this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the create method for the viewset
    def create(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new profile.
        """
        try:
            # Serialize the request data
            serializer = self.serializer_class(data=request.data)
            # Validate the serializer
            serializer.is_valid(raise_exception=True)
            # Create the profile instance
            self.perform_create(serializer)
            # Return the serialized data
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)