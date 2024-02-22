from rest_framework import serializers
from user.serializer import UserProfileSerializer, UserListSerializer
from issue.issueSerializer import IssueTypeSerializer, StatusSerializer, PrioritySerializer
from user.models import User, Role
from project.models import *
from issue.models import *


class AddTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def validate(self, data):
        team = Team.objects.filter(user_id=data['user'], project_id=data["project"]).first()
        if team:
            raise serializers.ValidationError("Member Already Exist")
        return data


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def validate(self, data):
        print(data)
        key = Project.objects.filter(key=data['key']).first()
        if key:
            raise serializers.ValidationError("This project Key is already in use")
        title = Project.objects.filter(title=data["title"]).first()
        if title:
            raise serializers.ValidationError("This project title is already in use")

        return data


class ProjectTeamSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return User.objects.filter(pk=obj.user_id).values('id', 'profile', 'fullName', "email", 'phoneNumber')

    class Meta:
        model = Team
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    team = ProjectTeamSerializer(read_only=True, many=True)
    issue = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        user = UserProfileSerializer(obj.created_by)
        return User.objects.filter(pk=user.data["id"]).values('id', 'profile', 'fullName')

    def get_issue(self, obj):
        issue = Issue.objects.filter(project_id=obj.id).values("id", "issue_summary")
        return issue

    class Meta:
        model = Project
        fields = '__all__'


class ProjectGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserProjectSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ["password"]


class AllProjectOfUserSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    def get_project(self, obj):
        projectid = Team.objects.filter(user_id=obj.id).values("project_id")
        project = list()
        for us in projectid:
            data = Project.objects.filter(id=us["project_id"]).all()
            seri = ProjectSerializer(data, many=True)
            project.append(seri.data)
        return project

    class Meta:
        model = User
        fields = '__all__'


class ProjectIssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    issue_type = IssueTypeSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    issueType = IssueTypeSerializer(read_only=True)
    assignee = UserListSerializer(read_only=True)
    priority = PrioritySerializer(read_only=True)

    class Meta:
        model = Issue
        fields = "__all__"


class TeamEmailAddress(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        user = User.objects.filter(pk=obj.user_id).values("email").first()
        return user

    class Meta:
        model = Issue
        fields = ["email"]


class IssueFilterSerializer(serializers.ModelSerializer):
    team = ProjectTeamSerializer(read_only=True, many=True)
    issue = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        user = UserProfileSerializer(obj.created_by)
        return User.objects.filter(pk=user.data["id"]).values('id', 'profile', 'fullName')

    def get_issue(self, obj):
        issue = Issue.objects.filter(project_id=obj.id).values("id", "issue_summary")
        return issue

    class Meta:
        model = Project
        fields = '__all__'
