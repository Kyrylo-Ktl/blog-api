"""Available URL"""

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ResetPasswordConfirm,
    ResetPasswordEmailRequest,
    UserCreateView,
    UserDetailView,
)

get_without_auth_schema = swagger_auto_schema(method='get', security=[])
post_without_auth_schema = swagger_auto_schema(method='post', security=[])
get_and_post_without_auth_schema = swagger_auto_schema(methods=['get', 'post'], security=[])

urlpatterns = [
    path('token/', post_without_auth_schema(TokenObtainPairView.as_view()), name='tokens'),
    path('token/refresh/', post_without_auth_schema(TokenRefreshView.as_view()), name='token-refresh'),

    path('signup/', post_without_auth_schema(UserCreateView.as_view()), name='signup'),
    path('profile/', UserDetailView.as_view(), name='profile'),

    path('password-reset/request/', post_without_auth_schema(ResetPasswordEmailRequest.as_view()), name='request-reset'),
    path('password-reset/<uuid>/<token>/', get_and_post_without_auth_schema(ResetPasswordConfirm.as_view()), name='confirm-reset'),
]
