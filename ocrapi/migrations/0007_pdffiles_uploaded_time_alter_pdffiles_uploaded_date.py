# Generated by Django 4.2.4 on 2023-12-26 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocrapi', '0006_alter_pdffiles_uploaded_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdffiles',
            name='uploaded_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='pdffiles',
            name='uploaded_date',
            field=models.DateField(),
        ),
    ]