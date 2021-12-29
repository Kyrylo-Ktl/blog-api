# Generated by Django 4.0 on 2021-12-29 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Category name', max_length=128, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(help_text='Comment text', max_length=512, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(help_text='Post text', max_length=1024, validators=[django.core.validators.MinLengthValidator(128)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Post title', max_length=128, unique=True, validators=[django.core.validators.MinLengthValidator(16)]),
        ),
    ]
