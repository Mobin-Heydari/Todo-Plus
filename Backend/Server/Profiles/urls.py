# Import the necessary modules
from django.urls import path, include

# Import the custom routers
from .routers import ProfileRouter, ProfileSecurityAuthenticationRouter, ProfileSocialMediaRouter

app_name = "Profiles"

# Create instances of the custom routers
profile_router = ProfileRouter()
profile_security_authentication_router = ProfileSecurityAuthenticationRouter()
profile_social_media_router = ProfileSocialMediaRouter()

# Define the URL patterns
urlpatterns = [
    path('', include(profile_router.get_urls())),
    path('security-authentications/', include(profile_security_authentication_router.get_urls())),
    path('social-medias/', include(profile_social_media_router.get_urls())),
]