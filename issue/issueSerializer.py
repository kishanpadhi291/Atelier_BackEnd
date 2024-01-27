from rest_framework import serializers
from issue.models import *
from project.models import Project,Team
from user.models import User
from django.db.models import Q
class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueType
        fields = "__all__"
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = "__all__"
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

class CreateCommentatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
class CommentSerializer(serializers.ModelSerializer):
    commentator = serializers.SerializerMethodField()

    def get_commentator(self, obj):
        print(obj.user_id)
        return User.objects.filter(email=obj.user_id).values('id', 'profile', 'fullName')

    class Meta:
        model = Comment
        fields = "__all__"
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"
class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"


class ProjectTeamSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,obj):
        return User.objects.filter(pk=obj.user_id).values('id','profile','fullName').first()

    class Meta:
        model = Team
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()
    status = StatusSerializer(read_only=True)
    priority = PrioritySerializer(read_only=True)
    issue_type = IssueTypeSerializer(read_only=True)
    comment = CommentSerializer(read_only=True,partial=True,many=True)
    attachment = AttachmentSerializer(partial=True,many=True)
    activityLog = ActivityLogSerializer(read_only=True,partial=True,many=True)

    def get_project(self,obj):
        project = Project.objects.filter(pk=obj.project_id).values("id","title","key")
        return project

    def get_team(self,obj):
        serializer = ProjectTeamSerializer(Team.objects.filter(project__id=obj.project_id), many=True)
        return serializer.data

    def get_assignee(self,obj):
        assignee = User.objects.filter(email=obj.assignee).values('id','profile','fullName')
        return assignee

    def get_reporter(self,obj):
        reporter = User.objects.filter(email=obj.reporter).values('id','profile','fullName')
        return reporter
    class Meta:
        model = Issue
        fields = "__all__"

class IssueCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id', 'issue_summary', 'issue_description', 'priority', 'status', 'assignee', 'reporter',
                  'project','issue_type', 'created_date', 'updated_date',"index")


class IssueBasicDetails(serializers.ModelSerializer):
    issue_type = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_issue_type(self,obj):
        issue_type = IssueTypeSerializer(IssueType.objects.get(pk=obj.issue_type.id))
        return issue_type.data

    def get_project(self,obj):
        project = Project.objects.filter(pk=obj.project.id).values("id","key","title").first()
        return project

    def get_status(self,obj):
        issue_status = StatusSerializer(Status.objects.get(pk=obj.status.id))
        return issue_status.data

    class Meta:
        model = Issue
        exclude = ["issue_description","index","created_date","reporter","assignee","priority"]

class GroupViseIssueSerializer(serializers.ModelSerializer):
    assignedIssue = serializers.SerializerMethodField()
    reportedIssue = serializers.SerializerMethodField()
    allIssue = serializers.SerializerMethodField()

    def get_allIssue(self,obj):
        issue = IssueBasicDetails(Issue.objects.filter(Q(assignee=obj.id) | Q(reporter=obj.id)), many=True)
        return issue.data

    def get_assignedIssue(self,obj):
        issue = IssueBasicDetails(Issue.objects.filter(assignee=obj.id),many=True)
        return issue.data

    def get_reportedIssue(self,obj):
        issue = IssueBasicDetails(Issue.objects.filter(reporter=obj.id),many=True)
        return issue.data

    class Meta:
        model = User
        exclude = ["password","user_permissions","last_login","is_active","is_staff","is_superuser","groups","is_verified"]

class IssueImportSerializer(serializers.Serializer):
    issue_summary = serializers.CharField()
    issue_description = serializers.CharField()
    project = serializers.CharField()
    assignee = serializers.EmailField()
    issue_type = serializers.CharField()
    priority = serializers.CharField()
    reporter = serializers.EmailField()
    status = serializers.CharField()

    def create(self, validated_data):
        project_key = validated_data.pop('project')
        assignee_email = validated_data.pop('assignee')
        issue_type_name = validated_data.pop('issue_type')
        priority_name = validated_data.pop('priority')
        reporter_email = validated_data.pop('reporter')
        status_name = validated_data.pop('status')

        project = Project.objects.get(key=project_key)
        assignee = User.objects.get(email=assignee_email)
        issue_type = IssueType.objects.get(name=issue_type_name)
        priority = Priority.objects.get(name=priority_name)
        reporter = User.objects.get(email=reporter_email)
        status = Status.objects.get(name=status_name)
        issue = Issue.objects.create(
            project=project,
            assignee=assignee,
            issue_type=issue_type,
            priority=priority,
            reporter=reporter,
            status=status,
            index='0',
            **validated_data
        )
        return issue