from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenObtainSerializer




class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer
    