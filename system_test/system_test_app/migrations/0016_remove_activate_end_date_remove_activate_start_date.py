# Generated by Django 5.1 on 2024-08-10 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0015_alter_activate_end_date_alter_activate_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activate',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='activate',
            name='start_date',
        ),
    ]
