# Generated by Django 5.0.2 on 2024-05-01 20:29

import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cover',
            field=models.ImageField(null=True, upload_to=store.models.path_and_rename),
        ),
    ]
