from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "me/",
        ManageUserView.as_view(actions={"get": "retrieve", "put": "update"}),
        name="manage",
    ),
    path(
        "me/upload-user-image/",
        ManageUserView.as_view(actions={"post": "upload_user_image"}),
        name="upload-user-image",
    ),
]

app_name = "user"
