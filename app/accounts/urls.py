"""Available URL"""

from django.urls import path
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


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='tokens'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('signup/', UserCreateView.as_view(), name='signup'),
    path('profile/', UserDetailView.as_view(), name='profile'),

    path('password-reset/request/', ResetPasswordEmailRequest.as_view(), name='request-reset'),
    path('password-reset/<uuid>/<token>/', ResetPasswordConfirm.as_view(), name='confirm-reset'),
]
