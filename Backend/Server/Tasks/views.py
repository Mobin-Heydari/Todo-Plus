from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Tasks
from .serializers import TasksSerializer
from .permissions import IsTheTaksOwner



class UserTasksViewSet(ModelViewSet):
    """
        ViewSet for The User Tasks.
    """
    # Define the queryset for the viewset
    queryset = Tasks.objects.all()
    # Define the serializer for the viewset
    serializer_class = TasksSerializer
    # Define the permission for the viewset
    permission_classes = [IsAuthenticated, IsTheTaksOwner]
    # Define the lookup_field for the viewset
    lookup_field = 'slug'

    # Define the list method for the viewset
    def list(self, request):
        """
            Handel a get request for the list of the user tasks.
            params:
                - request: The request object.
            return:
                - Response: The response object with the list of the user tasks.
        """
        queryset = self.get_queryset()

        instance = queryset.filter(user=request.user)

        serializer = self.serializer_class(instance, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # Define the retrieve method for the viewset
    def retrive(self, request, slug):
        """
            Handel the get request for a single user task.
            params:
                - slug: The slug of the task.
                - request: The request object.
            return:
                - Response: The response object with the single user task.
        """
        # The get_object method will return the object that matches the lookup value
        instance = get_object_or_404(Tasks, slug=slug)
        # The serializer will serialize the instance
        serializer = self.serializer_class(instance, many=False)
        # Returning the task data witch is serialized by serializer
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # defining the create method for the viewset
    def create(self, request):
        """
            Handle the post request for creating a new task.
            params:
                - request: The request object.
            return:
                - Response: The response object with the created task.
        """
        # Calling the serializer and giving the required data such as request as a context and data as a data request
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # caling the Validating method
        if serializer.is_valid():
            # Saving the task
            serializer.save()
            # Returning the task data witch is serialized by serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the task is not valid, returning the error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Defining the update mthod for the viewset
    def update(self, request, slug):
        """
            Handle the put request for updating the task for user.
            params:
                - request: The request object.
                - slug: The slug of the task.
            return:
                - Response: The response object with the updated task.
        """
        # The queryset is already defined in the viewset
        queryset = self.get_queryset()
        # The get_object method will return the object that matches the lookup value
        instance = get_object_or_404(Tasks, slug=slug, user=request.user)
        # The serializer will serialize the instance
        serializer = TasksSerializer(instance, data=request.data)
        # If the serializer is valid, saving the task
        if serializer.is_valid():
            # Saving the task
            serializer.save()
            # Returning the task data witch is serialized by serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If the task is not valid, returning the error message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Define the delete method for the viewset
    def delete(self, request, slug):
        """
            Handle the delete request for deleting the task for user.
            params:
                - request: The request object.
                - slug: The slug of the task.
            return:
                - Response: The response object with the message of the task deletion.
        """
        # The get_object method will return the object that matches the lookup value
        instance = get_object_or_404(Tasks, slug=slug, user=request.user)
        # Deleting the instance
        self.perform_destroy(instance)
        # Returning the message of the task deletion
        return Response({'Message':'Task has been deleted.'}, status=status.HTTP_204_NO_CONTENT)