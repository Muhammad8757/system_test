# Generated by Django 5.1 on 2024-08-10 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0003_theme_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='user_id',
        ),
    ]
