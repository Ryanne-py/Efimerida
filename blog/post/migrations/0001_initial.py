# Generated by Django 4.0.4 on 2022-07-20 13:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(error_messages={'min_length': 'Post title must be longer than two characters'}, max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('post_text', models.TextField(error_messages={'min_length': 'Post content must be longer than 10 characters'}, validators=[django.core.validators.MinLengthValidator(10)])),
                ('post_created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_edit_date', models.DateTimeField(blank=True, null=True)),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_rubric', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='post.rubric', verbose_name='Rubric')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['post_edit_date'],
            },
        ),
    ]
