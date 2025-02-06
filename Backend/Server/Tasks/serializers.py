from rest_framework import serializers
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