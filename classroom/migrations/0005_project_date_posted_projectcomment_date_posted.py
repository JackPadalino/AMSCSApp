# Generated by Django 4.0.5 on 2022-10-21 03:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_projecttopic_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='projectcomment',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
