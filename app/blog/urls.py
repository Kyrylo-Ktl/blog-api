"""Available URL"""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

schema_view = get_schema_view(
    openapi.Info(title='Blog API', default_version='v1', ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('', views.api_root),
    path('doc/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),

    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name="category-detail"),

    path('posts/', views.PostListView.as_view(), name='posts-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    path('comments/', views.CommentListView.as_view(), name='comments-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]
