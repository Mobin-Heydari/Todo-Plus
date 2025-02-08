from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .models import Tasks
from .serializers import TasksSerializer




class UserTasksViewSet(ViewSet):
    def list(self, request):
        queryset = Tasks.objects.all()
        instance = queryset.filter(user=request.user)
        serializer = TasksSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrive(self, request, slug):
        queryset = Tasks.objects.all()
        instance = queryset.filter(user=request.user, slug=slug)
        serializer = TasksSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = TasksSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, slug):
        instance = get_object_or_404(Tasks, slug=slug, user=request.user)
        serializer = TasksSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug):
        instance = get_object_or_404(Tasks, slug=slug, user=request.user)
        instance.delete()
        return Response({'Massage':'Task has been deleted.'}, status=status.HTTP_204_NO_CONTENT)