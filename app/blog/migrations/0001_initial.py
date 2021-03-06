# Generated by Django 4.0 on 2022-01-05 10:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Category name', max_length=128, unique=True, validators=[django.core.validators.MinLengthValidator(4)])),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Post title', max_length=128, unique=True, validators=[django.core.validators.MinLengthValidator(16)])),
                ('text', models.CharField(help_text='Post text', max_length=1024, validators=[django.core.validators.MinLengthValidator(128)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(help_text='Post author', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='accounts.user', verbose_name='author')),
                ('category', models.ForeignKey(help_text='Post category', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Comment text', max_length=512, validators=[django.core.validators.MinLengthValidator(8)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(help_text='Comment author', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.user', verbose_name='author')),
                ('post', models.ForeignKey(help_text='Comment post', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='post')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('-created_at',),
            },
        ),
    ]
