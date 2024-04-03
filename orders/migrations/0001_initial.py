# Generated by Django 5.0.2 on 2024-05-02 02:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_remove_orderproduct_quantities'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_order_id', models.CharField(max_length=22, unique=True)),
                ('payment_id', models.CharField(max_length=20, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('signature', models.CharField(max_length=64, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]