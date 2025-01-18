from django.urls import path
from users.views import (SendCodeAPIView,
                         VerifyCodeAPIView,
                         UserListAPIView,
                         UserRetrieveAPIView,
                         ActivateInviteCodeView,
                         UserUpdateAPIView,
                         SendCodeView, Home, VerifyCodeView, UserDetailView, ActivateInviteCodeTempView)
from users.apps import UsersConfig
from django.contrib.auth import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view(), name="send-code"),
    path("verify-code/", VerifyCodeAPIView.as_view(), name="verify-code"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", UserListAPIView.as_view(), name="users"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("activate_invite_code/", ActivateInviteCodeView.as_view(), name="activate-invite-code"),
    path("send_code/temp/", SendCodeView.as_view(), name="send-code-temp"),
    path("verify_code/temp/", VerifyCodeView.as_view(), name="verify-code-temp"),
    path("home/", Home.as_view(), name="home"),
    path("detail-temp/<int:pk>/", UserDetailView.as_view(), name="profile-temp"),
    path("activate_invite_code_temp/", ActivateInviteCodeTempView.as_view(), name="activate-invite-code-temp"),

]
