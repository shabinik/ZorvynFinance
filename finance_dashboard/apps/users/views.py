from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenSerializer
from .permissions import IsAdmin
from apps.core.responses import success

User = get_user_model()

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = [CustomTokenSerializer]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success(response.data, message="Login successful")
    

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success(message="Logged Out")
        except Exception:
            return success(message="Invalid token")



# ADMIN USER MANAGEMENT
# create view
# list view
# retrieve view
# update view
# delete view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = UserSerializer(request.user)
        return success(serializer.data)
    
    def partial_update(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success(serializer.data, message="Profile updated")
