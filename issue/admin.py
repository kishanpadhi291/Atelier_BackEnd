from django.contrib import admin
from issue.models import *
@admin.register(Issue)
class Issue(admin.ModelAdmin):
    list_display = ["id",'status','issue_summary','project_id',
                    'issue_description','priority','assignee','reporter',
                    'issue_type','created_date','updated_date']
@admin.register(IssueType)
class IssueType(admin.ModelAdmin):
    list_display = ['id','name','icon']
@admin.register(Priority)
class Priority(admin.ModelAdmin):
    list_display = ['id','name','icon']
@admin.register(Status)
class Status(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['id','issue_id','user_id','comment_text','created_date']
@admin.register(ActivityLog)
class ActivityLog(admin.ModelAdmin):
    list_display = ['id','issue_id','user_id','activityType','prev','latest','created_date']
@admin.register(Attachment)
class Attachment(admin.ModelAdmin):
    list_display = ["id","issue_id","attachment_file","created_date"]

