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