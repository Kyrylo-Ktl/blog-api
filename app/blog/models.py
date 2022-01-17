"""The module is used to describe database models"""

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class BaseModel(models.Model):
    """Abstract base class for optimizing writing of all models"""

    @classmethod
    def get_all(cls) -> models.QuerySet:
        return cls.objects.all()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(BaseModel):
    """Entity Model Category"""

    name = models.CharField(max_length=128, unique=True, help_text='Category name',
                            validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(BaseModel):
    """Entity Model Post"""

    title = models.CharField(max_length=128, unique=True, help_text='Post title',
                             validators=[MinLengthValidator(16)])
    text = models.CharField(max_length=1024, help_text='Post text',
                            validators=[MinLengthValidator(128)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='author', on_delete=models.CASCADE,
                               related_name='posts', help_text='Post author')
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE,
                                 related_name='posts', help_text='Post category')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(BaseModel):
    """Entity Model Comment"""

    text = models.CharField(max_length=512, help_text='Comment text',
                            validators=[MinLengthValidator(8)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE,
                             related_name='comments', help_text='Comment post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='author', on_delete=models.CASCADE,
                               related_name='comments', help_text='Comment author')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
