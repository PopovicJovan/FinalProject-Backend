# Generated by Django 4.2.5 on 2023-10-01 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0008_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
