from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer
from .permissions import IsStaffOrSelf, IsStaff, IsSelf



# Define a viewset for the User model
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the User model.
    """
    # Define the queryset for the viewset
    queryset = User.objects.all()
    # Define the serializer class for the viewset
    serializer_class = UserSerializer
    # Define the permission classes for the viewset
    permission_classes = [IsAuthenticated, IsStaffOrSelf]
    # Defines the required field for retrive methods
    lookup_field = 'username'

    # Define the list method for the viewset
    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve a list of users.
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
    def retrieve(self, request, username, *args, **kwargs):
        """
        Handle GET requests to retrieve a single user.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.is_staff or request.user.username == username:
                # Retrieve the user instance
                queryset = get_object_or_404(User, username=username)
                # Serialize the user instance
                serializer = self.get_serializer(queryset)
                # Return the serialized data
                return Response(serializer.data)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to view this content"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            # Return a 404 Not Found response if the user does not exist
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define the update method for the viewset
    def update(self, request, username, *args, **kwargs):
        """
        Handle PATCH requests to update a single user.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == username or request.user.is_staff:
                # Retrieve the user instance
                instance = get_object_or_404(User, username=username)
                # Serialize the user instance
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                # Validate the serializer
                serializer.is_valid(raise_exception=True)
                # Update the user instance
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
    def destroy(self, request, username, *args, **kwargs):
        """
        Handle DELETE requests to delete a single user.
        """
        try:
            # Check if the user is staff or the user themselves
            if request.user.username == username or request.user.is_staff:
                # Retrieve the user instance
                instance = get_object_or_404(User, username=username)
                # Delete the user instance
                self.perform_destroy(instance)
                # Return a 204 No Content response
                return Response({"Detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Return a 403 Forbidden response if the user is not staff or the user themselves
                return Response({"error": "You do not have permission to delete this content"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Return a 500 Internal Server Error response if an exception occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)