from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Profile, ProfileSecurityAuthentication, ProfileSocialMedia
from .serializers import ProfileSerializer, ProfileSocialMediaSerializer, ProfileSecurityAuthenticationSerializer

class ProfileViewSet(viewsets.ViewSet):
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
                queryset = self.get_queryset()
                # Serialize the queryset
                serializer = self.get_serializer(queryset, many=True)
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
                # Retrieve the profile instance
                queryset = get_object_or_404(Profile, user_username=user_username)
                # Serialize the profile instance
                serializer = self.get_serializer(queryset)
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
        """
        Handle PATCH requests to update a single profile.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == user_username or request.user.is_staff:
                # Retrieve the profile instance
                instance = get_object_or_404(Profile, user_username=user_username)
                # Serialize the profile instance
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                # Validate the serializer
                serializer.is_valid(raise_exception=True)
                # Update the profile instance
                self.perform_update(serializer)
                # Return the serialized data
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to update this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the destroy method for the viewset
    def destroy(self, request, user_username, *args, **kwargs):
        """
        Handle DELETE requests to delete a single profile.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == user_username or request.user.is_staff:
                # Retrieve the profile instance
                instance = get_object_or_404(Profile, user_username=user_username)
                # Delete the profile instance
                self.perform_destroy(instance)
                # Return a 204 No Content response
                return Response({"Detail": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to delete this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileSecurityAuthenticationViewSet(viewsets.ViewSet):
    """
    ViewSet for the ProfileSecurityAuthentication model.
    """
    # Define the queryset for the viewset
    queryset = ProfileSecurityAuthentication.objects.all()
    # Define the serializer class for the viewset
    serializer_class = ProfileSecurityAuthenticationSerializer
    # Define the permission classes for the viewset
    permission_classes = [IsAuthenticated]
    # Defines the required field for retrieve methods
    lookup_field = 'profile__user__username'

    # Define the list method for the viewset
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve a list of profile security authentications.
        """
        try:
            # Check if the user is staff
            if request.user.is_staff:
                # Retrieve the queryset
                queryset = self.get_queryset()
                # Serialize the queryset
                serializer = self.get_serializer(queryset, many=True)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the retrieve method for the viewset
    def retrieve(self, request, profile__user__username, *args, **kwargs):
        """
        Handle GET requests to retrieve a single profile security authentication.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.is_staff or request.user.username == profile__user__username:
                # Retrieve the profile security authentication instance
                queryset = get_object_or_404(ProfileSecurityAuthentication, profile__user__username=profile__user__username)
                # Serialize the profile security authentication instance
                serializer = self.get_serializer(queryset)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except ProfileSecurityAuthentication.DoesNotExist:
            # Return a 404 Not Found response if the profile security authentication does not exist
            return Response({"error": "Profile security authentication not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the update method for the viewset
    def update(self, request, profile__user__username, *args, **kwargs):
        """
        Handle PATCH requests to update a single profile security authentication.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == profile__user__username or request.user.is_staff:
                # Retrieve the profile security authentication instance
                instance = get_object_or_404(ProfileSecurityAuthentication, profile__user__username=profile__user__username)
                # Serialize the profile security authentication instance
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                # Validate the serializer
                serializer.is_valid(raise_exception=True)
                # Update the profile security authentication instance
                self.perform_update(serializer)
                # Return the serialized data
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to update this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProfileSocialMediaViewSet(viewsets.ViewSet):
    """
    ViewSet for the ProfileSocialMedia model.
    """
    # Define the queryset for the viewset
    queryset = ProfileSocialMedia.objects.all()
    # Define the serializer class for the viewset
    serializer_class = ProfileSocialMediaSerializer
    # Define the permission classes for the viewset
    permission_classes = [IsAuthenticated]
    # Defines the required field for retrieve methods
    lookup_field = 'profile__user__username'

    # Define the list method for the viewset
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve a list of profile social media.
        """
        try:
            # Check if the user is staff
            if request.user.is_staff:
                # Retrieve the queryset
                queryset = self.get_queryset()
                # Serialize the queryset
                serializer = self.get_serializer(queryset, many=True)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the retrieve method for the viewset
    def retrieve(self, request, profile__user__username, *args, **kwargs):
        """
        Handle GET requests to retrieve a single profile social media.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.is_staff or request.user.username == profile__user__username:
                # Retrieve the profile social media instance
                queryset = get_object_or_404(ProfileSocialMedia, profile__user__username=profile__user__username)
                # Serialize the profile social media instance
                serializer = self.get_serializer(queryset)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except ProfileSocialMedia.DoesNotExist:
            # Return a 404 Not Found response if the profile social media does not exist
            return Response({"error": "Profile social media not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the update method for the viewset
    def update(self, request, profile__user__username, *args, **kwargs):
        """
        Handle PATCH requests to update a single profile social media.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == profile__user__username or request.user.is_staff:
                # Retrieve the profile social media instance
                instance = get_object_or_404(ProfileSocialMedia, profile__user__username=profile__user__username)
                # Serialize the profile social media instance
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                # Validate the serializer
                serializer.is_valid(raise_exception=True)
                # Update the profile social media instance
                self.perform_update(serializer)
                # Return the serialized data
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to update this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)