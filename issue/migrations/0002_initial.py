# Generated by Django 5.0 on 2023-12-29 09:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issue', '0001_initial'),
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='project.project'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='issue.issue'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='issue.issue'),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activityLog', to='issue.issue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='issue_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_type', to='issue.issuetype'),
        ),
        migrations.AddField(
            model_name='issue',
            name='priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='priority', to='issue.priority'),
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='issue.status'),
        ),
    ]
