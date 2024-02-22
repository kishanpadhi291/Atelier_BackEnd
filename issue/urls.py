from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("issue-type", IssueTypeCRUDVIEW.as_view(), name="issue-type"),
    path("issue-priority", PriorityCRUDVIEW.as_view(), name="issue-priority"),
    path("issue-status", StatusCRUDVIEW.as_view(), name="issue-status"),
    path("issue-comment", CommentCRUDVIEW.as_view(), name="issue-comment"),
    path("issue-attachment", AttachmentCRUDVIEW.as_view(), name="issue-attachment"),
    path("issue-activityLog", ActivityLogCRUDVIEW.as_view(), name="issue-activityLog"),
    path("issue-delete/<int:pk>", IssueCRUDVIEW.as_view(), name="issues"),
    path("issues", IssueCRUDVIEW.as_view(), name="issues"),
    path("issue-update/<int:issue_id>", UpdateIssueFields.as_view(), name="update-issues"),
    path("issue-comment-create", PostCommentIssue().as_view(), name="create-comment"),
    path("issue-comment-delete/<int:pk>", PostCommentIssue().as_view(), name="delete-comment"),
    path("issue-comment-update/<int:pk>", PostCommentIssue().as_view(), name="update-comment"),
    path("upload-issues", UploadCsvIssues.as_view(), name="upload-issues"),
    path("issue-filter", IssueFilterView.as_view(), name="issue-filter"),
    path("issue-filter-id/<str:id>", IssueFilterByIdView.as_view(), name="issue-filter-id")
]
