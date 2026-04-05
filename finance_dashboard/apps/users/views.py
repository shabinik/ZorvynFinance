from rest_framework import viewsets,status,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenSerializer,RegisterSerializer
from .permissions import IsAdmin
from apps.core.responses import success,error
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

User = get_user_model()

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request,*args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return success(
            data={
                "id": user.id,
                "email": user.email,
                "role": user.role,  # will always be "viewer"
            },
            message="Account created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

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
            return error(message="Invalid token")



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

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ["role","is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["date_joined","email"]
    ordering = ["-date_joined"]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        if user == request.user:
            return error(
                message="You cannot deactivate your own account.",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        user.is_active = False
        user.save(update_fields = ["is_active"])
        return success(message=f"User {user.email} has been deactivated.")


class ProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = UserSerializer(request.user)
        return success(serializer.data)
    
    def partial_update(self, request,pk = None):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success(serializer.data, message="Profile updated")
