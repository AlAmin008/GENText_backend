# Generated by Django 4.2.4 on 2023-12-10 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocrapi', '0005_alter_pdffiles_total_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdffiles',
            name='uploaded_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
