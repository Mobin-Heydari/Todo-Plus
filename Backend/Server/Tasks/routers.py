# Import the necessary modules
from rest_framework import routers
from django.urls import path, include

from .views import UserTasksViewSet


# Define a custom router class for the UserTasksViewSet
class UserTasksRouter(routers.DefaultRouter):
    # Initialize the custom router
    def __init__(self):
        super().__init__()
        # Register the UserTasksViewSet with the custom router
        self.register(r'', UserTasksViewSet, basename='user-tasks')

    # Define a method to get the URLs for the custom router
    def get_urls(self):
        
        # Get the URLs from the parent class
        urls = super().get_urls()

        # Define custom URLs for the UserTasksViewSet
        custom_urls = [
            # Define a URL pattern for the list view
            path('user-tasks/', include([

                # Define a URL pattern for the list view
                path('', UserTasksViewSet.as_view({'get': 'list'})),

                # Define a URL pattern for the create view
                path('create/', UserTasksViewSet.as_view({'post': 'create'})),

                # Define a URL pattern for the detail view
                path('<str:user_username>/', include([

                    # Define a URL pattern for the detail view
                    path('', UserTasksViewSet.as_view({'get': 'retrieve'})),

                    # Define a URL pattern for the update view
                    path('update/', UserTasksViewSet.as_view({'put': 'update'})),

                    # Define a URL pattern for the delete view
                    path('delete/', UserTasksViewSet.as_view({'delete': 'destroy'})),

                ])),
            ]))
        ]
        # Return the custom URLs
        return urls + custom_urls