from django.urls import path
from users.views import SendCodeAPIView, VerifyCodeAPIView
from users.apps import UsersConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view(), name="send-code"),
    path("verify-code/", VerifyCodeAPIView.as_view(), name="verify-code"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
