"""Available URL"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.api_root),

    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name="category-detail"),

    path('posts/', views.PostListView.as_view(), name='posts-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    path('comments/', views.CommentListView.as_view(), name='comments-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]
