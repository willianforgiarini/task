from django.urls import path
from .views import UserRegistrationView, ChangePasswordView, UserListView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    # retorna um token para acessar a api, e um refresh_token
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # o refresh_token é usado nesse endpoint, retornando um token novo, assim não é preciso fazer um novo login
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("user/<int:id>/", UserDetailView.as_view(), name="user-detail")
]

