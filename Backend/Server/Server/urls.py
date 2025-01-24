from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("Users.urls", namespace="Users")),
    path('auth/', include("Authentication.urls", namespace="Authentication")),
    path('profiles/', include("Profiles.urls", namespace="Profiles")),
]
