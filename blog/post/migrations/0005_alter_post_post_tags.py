# Generated by Django 4.2.2 on 2023-07-28 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_tag_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_tags',
            field=models.ManyToManyField(blank=True, to='post.tag'),
        ),
    ]
