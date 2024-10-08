# Generated by Django 5.1 on 2024-08-10 08:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_test_app', '0021_activate_end_date_activate_start_date'),
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
        migrations.RemoveField(
            model_name='activate',
            name='subject_id',
        ),
        migrations.RemoveField(
            model_name='activate',
            name='tests_id',
        ),
        migrations.RemoveField(
            model_name='activate',
            name='user_id',
        ),
        migrations.AddField(
            model_name='activate',
            name='date_end',
            field=models.CharField(default='0', max_length=25),
        ),
        migrations.AddField(
            model_name='activate',
            name='date_start',
            field=models.CharField(default='0', max_length=25),
        ),
        migrations.AddField(
            model_name='activate',
            name='id_theme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system_test_app.theme'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_activated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_test_app.activate')),
                ('id_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
