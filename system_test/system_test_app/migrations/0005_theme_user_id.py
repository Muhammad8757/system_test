# Generated by Django 5.1 on 2024-08-10 05:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0004_remove_theme_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='user_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
