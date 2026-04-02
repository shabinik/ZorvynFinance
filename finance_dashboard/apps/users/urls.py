from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, ProfileView, LoginView

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    # Auth
    path("auth/login/", LoginView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),

    # Users
    path("", include(router.urls)),

    # Profile
    path("me/", ProfileView.as_view({
        "get": "list",
        "patch": "partial_update",
    })),
]