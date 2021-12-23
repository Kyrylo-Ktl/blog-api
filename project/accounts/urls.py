"""Available URL"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='tokens'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('profile/', views.UserDetailView.as_view(), name='profile'),
]
