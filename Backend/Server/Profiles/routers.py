# Import the necessary modules
from rest_framework import routers
from django.urls import path, include

from .views import ProfileViewSet, ProfileSecurityAuthenticationViewSet, ProfileSocialMediaViewSet


# Define a custom router class for the ProfileViewSet
class ProfileRouter(routers.DefaultRouter):
    # Initialize the custom router
    def __init__(self):
        super().__init__()
        # Register the ProfileViewSet with the custom router
        self.register(r'', ProfileViewSet, basename='profiles')

    # Define a method to get the URLs for the custom router
    def get_urls(self):
        # Get the URLs from the parent class
        urls = super().get_urls()
        # Define custom URLs for the ProfileViewSet
        custom_urls = [
            # Define a URL pattern for the list view
            path('', include([
                # Define a URL pattern for the list view
                path('', ProfileViewSet.as_view({'get': 'list'})),
                # Define a URL pattern for the detail view
                path('<str:user_username>/', include([
                    # Define a URL pattern for the detail view
                    path('', ProfileViewSet.as_view({'get': 'retrieve'})),
                    # Define a URL pattern for the update view
                    path('update/', ProfileViewSet.as_view({'put': 'update'})),
                    # Define a URL pattern for the delete view
                    path('delete/', ProfileViewSet.as_view({'delete': 'destroy'})),
                ])),
            ])),
        ]
        # Return the custom URLs
        return urls + custom_urls


# Define a custom router class for the ProfileSecurityAuthenticationViewSet
class ProfileSecurityAuthenticationRouter(routers.DefaultRouter):
    # Initialize the custom router
    def __init__(self):
        super().__init__()
        # Register the ProfileSecurityAuthenticationViewSet with the custom router
        self.register(r'', ProfileSecurityAuthenticationViewSet, basename='security-authentications')

    # Define a method to get the URLs for the custom router
    def get_urls(self):
        # Get the URLs from the parent class
        urls = super().get_urls()
        # Define custom URLs for the ProfileSecurityAuthenticationViewSet
        custom_urls = [
            # Define a URL pattern for the list view
            path('', include([
                # Define a URL pattern for the list view
                path('', ProfileSecurityAuthenticationViewSet.as_view({'get': 'list'})),
                # Define a URL pattern for the detail view
                path('<str:profile__user__username>/', include([
                    # Define a URL pattern for the detail view
                    path('', ProfileSecurityAuthenticationViewSet.as_view({'get': 'retrieve'})),
                    # Define a URL pattern for the update view
                    path('update/', ProfileSecurityAuthenticationViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        # Return the custom URLs
        return urls + custom_urls


# Define a custom router class for the ProfileSocialMediaViewSet
class ProfileSocialMediaRouter(routers.DefaultRouter):
    # Initialize the custom router
    def __init__(self):
        super().__init__()
        # Register the ProfileSocialMediaViewSet with the custom router
        self.register(r'', ProfileSocialMediaViewSet, basename='social-medias')

    # Define a method to get the URLs for the custom router
    def get_urls(self):
        # Get the URLs from the parent class
        urls = super().get_urls()
        # Define custom URLs for the ProfileSocialMediaViewSet
        custom_urls = [
            # Define a URL pattern for the list view
            path('', include([
                # Define a URL pattern for the list view
                path('', ProfileSocialMediaViewSet.as_view({'get': 'list'})),
                # Define a URL pattern for the detail view
                path('<str:profile__user__username>/', include([
                    # Define a URL pattern for the detail view
                    path('', ProfileSocialMediaViewSet.as_view({'get': 'retrieve'})),
                    # Define a URL pattern for the update view
                    path('update/', ProfileSocialMediaViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        # Return the custom URLs
        return urls + custom_urls