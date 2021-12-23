"""Module for describing model views"""

from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Category, Comment, Post
from .permissions import IsAdminUser, IsAuthorUser, ReadOnly
from .serializers import CategorySerializer, CommentSerializer, PostSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('categories-list', request=request, format=format),
        'posts': reverse('posts-list', request=request, format=format),
        'comments': reverse('comments-list', request=request, format=format),
        'signup': reverse('signup', request=request, format=format),
        'profile': reverse('profile', request=request, format=format),
        'token': reverse('tokens', request=request, format=format),
        'token_refresh': reverse('token-refresh', request=request, format=format),
    })


class CategoryListView(ListCreateAPIView):
    """
    View to display all categories.
    Only admin can add a new one
    """
    queryset = Category.get_all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminUser]


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    Presentation to return category by ID.
    Only admin can update category information or delete category
    """
    queryset = Category.get_all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminUser]


class PostListView(ListCreateAPIView):
    """
    View to display all posts.
    Only an authorized user can add a new one
    """
    queryset = Post.get_all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """
    Presentation to return post by ID.
    Only post author and admin have option to update post information or delete post
    """
    queryset = Post.get_all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnly | IsAuthorUser | IsAdminUser]


class CommentListView(ListCreateAPIView):
    """
    View to display all comments.
    Only authorized user can add a new one
    """
    queryset = Comment.get_all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Presentation to return comment by ID
    Only comment author and admin have option to update comment information or delete comment
    """
    queryset = Comment.get_all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | IsAuthorUser | IsAdminUser]
