# Generated by Django 5.1.5 on 2025-01-25 19:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Authentication', '0002_delete_blacklistedtoken'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimePassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=250, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_time_passwords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'One Time Password',
                'verbose_name_plural': 'One Time Passwords',
            },
        ),
    ]
