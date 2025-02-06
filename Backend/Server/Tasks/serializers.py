from rest_framework import serializers
from django.utils.crypto import get_random_string

from .models import Tasks



class TasksSerializer(serializers.ModelSerializer):

    # Useing the method field to create a read-only field that returns the username
    user = serializers.SerializerMethodField()

    # Defining the fields that will be serialized
    class Meta:
        model = Tasks
        fields = '__all__'

    # Getting the username instead of user id
    def get_user(self, obj):
        return obj.user.username
    

    def create(self, validated_data):
        # Geting the request object through the context
        request = self.context.get('request')
        # Geting the user by request 
        user = request.user

        # Using random string func to generate a random string for slug field
        slug = get_random_string(255)
        
        # Creating the task query by validated data and other data that we got
        task = Tasks.objects.create(
            user=user,
            slug=slug,
            title=validated_data['title'],
            description=validated_data['description'],
            deadline=validated_data['deadline'],
        )
        # Saving the query 
        task.save()
        # Returning the query
        return task
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
    