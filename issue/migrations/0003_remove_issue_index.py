# Generated by Django 5.0 on 2024-01-05 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='index',
        ),
    ]
