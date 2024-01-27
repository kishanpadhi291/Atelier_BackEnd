from django.urls import path
from .views import *

urlpatterns = [
    path("CRUD/", UserProjectCRUD.as_view(), name="project-CRUD"),
    path("CRUD/<str:keys>", UserProjectCRUD.as_view(), name="project-CRUD-keys"),
    path("team/", TeamCrudView.as_view(), name="project-add-team"),
    path("team/<str:keys>", TeamCrudView.as_view(), name="project-team"),
    path("all-list-pagination/", AllProjectForUser.as_view(), name="all-project-pagination"),
    path("all-list/", AllProjectForUserWOP.as_view(), name="all-project"),
    path("custom-project-list/", CustomProjectForUser.as_view(), name="custom-all-project"),
    path("work/<str:keys>", ProjectIssueView.as_view(), name="project-issue")
]
