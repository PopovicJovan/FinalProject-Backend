# Generated by Django 4.2.5 on 2023-09-30 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0006_alter_blog_id_alter_comment_id_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
