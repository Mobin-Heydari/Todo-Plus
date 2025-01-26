from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("Users.urls", namespace="Users")),
    path('auth/', include("Authentication.urls", namespace="Authentication")),
    path('profiles/', include("Profiles.urls", namespace="Profiles")),
    path('accounts/', include("Accounts.urls", namespace="Accounts")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
