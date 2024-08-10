# Generated by Django 5.1 on 2024-08-10 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0025_alter_activate_id_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activate',
            name='id_theme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system_test_app.theme'),
            preserve_default=False,
        ),
    ]
