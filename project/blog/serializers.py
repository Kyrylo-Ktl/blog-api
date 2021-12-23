"""Module for describing serialization of models"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Post


class CategorySerializer(serializers.ModelSerializer):
    """Model serializer for Category class"""
    name = serializers.CharField(min_length=4, max_length=128,
                                 validators=[UniqueValidator(queryset=Category.get_all())])

    class Meta:
        model = Category
        fields = ('id', 'name',)


class PostSerializer(serializers.ModelSerializer):
    """Model serializer for Post class"""
    title = serializers.CharField(min_length=16, max_length=128,
                                  validators=[UniqueValidator(queryset=Post.get_all())])
    text = serializers.CharField(min_length=128, max_length=1024)

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    category = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.get_all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'created_at', 'updated_at', 'category', 'author',)


class CommentSerializer(serializers.ModelSerializer):
    """Model serializer for Comment class"""
    text = serializers.CharField(min_length=8, max_length=512)

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    post = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Post.get_all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_at', 'updated_at', 'post', 'author',)
