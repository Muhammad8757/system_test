# Generated by Django 5.1 on 2024-08-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0032_remove_activate_date_end_remove_activate_date_start_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='is_true',
            field=models.BooleanField(default=False),
        ),
    ]
