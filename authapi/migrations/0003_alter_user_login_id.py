# Generated by Django 4.2.4 on 2023-12-24 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapi', '0002_user_image_user_login_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_id',
            field=models.CharField(default=models.EmailField(max_length=255, unique=True, verbose_name='Email'), max_length=255, unique=True),
        ),
    ]
