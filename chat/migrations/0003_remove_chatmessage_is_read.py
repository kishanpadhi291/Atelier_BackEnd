# Generated by Django 5.0 on 2024-01-11 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_chatmessage_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='is_read',
        ),
    ]
