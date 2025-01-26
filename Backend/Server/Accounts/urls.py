from django.urls import path
from . import views

app_name = "Accounts"

# Define the URL patterns for the API
urlpatterns = [
    # URL pattern for generating a new OTP
    path('generate-otp/', views.GenerateOTPView.as_view(), name='generate-otp'),
]