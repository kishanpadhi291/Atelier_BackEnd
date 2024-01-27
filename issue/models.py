from django.db import models
from user.models import *
from project.models import *
from django.core.files.storage import FileSystemStorage
from cloudinary_storage.storage import MediaCloudinaryStorage
class Status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"

class Priority(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons/',storage=MediaCloudinaryStorage(), blank=True, max_length=1000)

    def __str__(self):
        return f"{self.name}"


class IssueType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icons/',storage=MediaCloudinaryStorage(), blank=True, max_length=1000)


    def __str__(self):
        return f"{self.name}"
class Issue(models.Model):
    issue_summary = models.CharField(max_length=200)
    issue_description = models.TextField()
    priority = models.ForeignKey(Priority,related_name="priority",on_delete=models.CASCADE)
    status = models.ForeignKey(Status,related_name="status",on_delete=models.CASCADE)
    assignee = models.ForeignKey(User,related_name="assignee",on_delete=models.CASCADE)
    reporter = models.ForeignKey(User,related_name="reporter",on_delete=models.CASCADE)
    project = models.ForeignKey(Project,related_name="projects",on_delete=models.CASCADE)
    issue_type = models.ForeignKey(IssueType,related_name="issue_type",on_delete=models.CASCADE)
    index = models.IntegerField()
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_date =models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.issue_summary}"

class Comment(models.Model):
    issue_id = models.ForeignKey(Issue,related_name="comment",on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,related_name="commentator",on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.comment_text}"

class ActivityLog(models.Model):
    issue_id = models.ForeignKey(Issue, related_name="activityLog", on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    activityType = models.TextField()
    prev = models.TextField()
    latest = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)


class Attachment(models.Model):
    issue_id = models.ForeignKey(Issue, related_name="attachment", on_delete=models.CASCADE)
    attachment_file = models.FileField(upload_to='documents/',max_length=1000,storage=FileSystemStorage())
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
