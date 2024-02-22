from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView,Response
from rest_framework.permissions import IsAuthenticated
from .projectSerializer import *
from issue.issueSerializer import *
from .models import *
from user.models import *
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView

class MyCustomPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 100


class UserProjectCRUD(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,keys):
        project = Project.objects.filter(key=keys).first()
        serializer = ProjectSerializer(project, read_only=True)
        return Response(serializer.data)

    def post(self,request):
        data = {
            "title":request.data['title'],
            "key":request.data['key'],
            "description":request.data['description'],
            "github": request.data['github'],
        }
        check=Project.objects.filter(Q(title=data['title']) | Q(key=data['key'])).exists()
        if not check:
            user = User.objects.get(id=request.user.id)
            Project.objects.create(title=data['title'], key=data['key'], description=data['description'],github=data['github'], created_by=user)
            lastCreatedProject = Project.objects.order_by('-start_date').first()
            role = Role.objects.order_by('id').first()
            team = Team()
            team.user = request.user
            team.project = lastCreatedProject
            team.role = role
            team.save()
            return Response({"success": "Project Created successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Title/Key already in used"})

    def put(self, request, keys):
        project = get_object_or_404(Project, id=keys)
        fields_to_update = ['title', 'key', 'description', 'github']
        updateData = {field: request.data.get(field, getattr(project, field)) for field in fields_to_update}
        updateData['start_date']=project.start_date
        updateData['created_by'] = project.created_by.id
        serializer = ProjectEditSerializer(project, data=updateData, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,keys):
        project = Project.objects.filter(pk=keys)
        project.delete()
        return Response({"success": "Project deleted successfully"})

class ProjectByName(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,tx):
        project = Project.objects.filter(title__icontains=tx)
        serializer = ProjectGetSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AllProjectForUser(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyCustomPagination

    def get(self,request):
        projectId = Team.objects.filter(user_id=request.user.id).values_list("project_id")
        project = Project.objects.filter(id__in=projectId)

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(project, request)

        data = ProjectSerializer(paginated_projects, many=True).data
        return paginator.get_paginated_response(data)

class AllProjectForTeamUser(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyCustomPagination

    def get(self,request,id):
        projectId = Team.objects.filter(user_id=id).values_list("project_id")
        project = Project.objects.filter(id__in=projectId)

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(project, request)

        data = ProjectSerializer(paginated_projects, many=True).data
        return paginator.get_paginated_response(data)

class AllProjectForUserWOP(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        projectId = Team.objects.filter(user_id=request.user.id).values_list("project_id")
        project = Project.objects.filter(id__in=projectId)
        serializer = ProjectSerializer(project, many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

class CustomProjectForUser(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyCustomPagination

    def post(self,request):
        projectId = Team.objects.filter(user_id=request.user.id).values_list("project_id")
        project = Project.objects.filter(Q(id__in=projectId) & Q(key__icontains=request.data["searchText"]) |
                                         Q(title__icontains=request.data["searchText"]))

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(project, request)

        data = ProjectSerializer(paginated_projects, many=True).data
        return paginator.get_paginated_response(data)

class ProjectIssueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,keys):
        serializer = ProjectIssueSerializer(Issue.objects.filter(project__key=keys), many=True)
        return Response({"data":serializer.data})

class TeamCrudView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,keys):
        serializer = ProjectTeamSerializer(Team.objects.filter(project__key=keys), many=True)
        return Response({"data":serializer.data})

    def post(self,request):
        data = {
            "project":int(request.data["project"]),
            "role":int(request.data["role"]),
            "user":request.data["user"],
        }
        serializer = AddTeamMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return Response({"Error": serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,keys):
        team=Team.objects.get(id=keys)
        team.delete()
        return Response({"data":"Member removed successfully"}, status=status.HTTP_200_OK)
