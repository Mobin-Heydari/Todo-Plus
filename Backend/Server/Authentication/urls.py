from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views



app_name = "authentication"


urlpatterns = [
    # Tokens 
    path('token/', views.TokenObtainView.as_view(), name="token_obtain"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # Login
    path('login/', views.LoginAPIView.as_view(), name="login"),
    # Logout
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
]