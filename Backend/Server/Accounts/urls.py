from django.urls import path
from . import views

app_name = "Accounts"

# Define the URL patterns for the API
urlpatterns = [
    # URL pattern for generating a new OTP
    path('account-verification-generate-otp/', views.AccountVerificationGenerateOTPView.as_view(), name='generate-otp'),
    path('account-verification/<str:token>/', views.AccountVerificationView.as_view(), name='account-verification'),
]