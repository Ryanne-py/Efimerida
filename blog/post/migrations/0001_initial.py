# Generated by Django 4.2.2 on 2023-06-29 12:25

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(error_messages={'max_length': 'The comment cannot be longer than 1000 characters'}, validators=[django.core.validators.MaxLengthValidator(1000)])),
                ('comment_created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-comment_created_date'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(error_messages={'min_length': 'Post title must be longer than two characters'}, max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('post_image', models.ImageField(blank=True, null=True, upload_to='post_image/%Y/%m/%d/')),
                ('post_text', models.TextField(error_messages={'min_length': 'Post content must be longer than 10 characters'}, validators=[django.core.validators.MinLengthValidator(10)])),
                ('post_created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_edit_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('post_views', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['post_edit_date'],
            },
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rubric_name', models.CharField(db_index=True, max_length=25)),
            ],
            options={
                'verbose_name': 'Rubric',
                'verbose_name_plural': 'Rubrics',
                'ordering': ['rubric_name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['tag_name'],
            },
        ),
    ]
