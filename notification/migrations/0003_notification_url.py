# Generated by Django 5.0 on 2024-01-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.CharField(default='kishan', max_length=500),
            preserve_default=False,
        ),
    ]