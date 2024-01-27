from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from project.projectSerializer import TeamEmailAddress,ProjectIssueSerializer
from issue.issueSerializer import *
from issue.models import *
from rest_framework.views import Response
from django.utils import timezone
import datetime
import pandas as pd
from django.db.models import Q

class IssueTypeCRUDVIEW(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = IssueType.objects.all()
    serializer_class = IssueTypeSerializer
class PriorityCRUDVIEW(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
class StatusCRUDVIEW(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
class CommentCRUDVIEW(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class AttachmentCRUDVIEW(APIView):
    serializer_class = AttachmentSerializer

    def post(self,request):
        data = {
            "attachment_file":request.FILES["attachment_file"],
            "issue_id":request.data["issue_id"]
        }
        serializer = AttachmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            attachment = Attachment.objects.filter(issue_id=request.data["issue_id"])
            serializer = AttachmentSerializer(attachment,many=True)
            return Response({"success":serializer.data})
        else:
            return Response({"error":serializer.errors})

class ActivityLogCRUDVIEW(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer

def send_email(subject,message,to_email):
    subject = subject
    body = f"<p style='font-size:20px;'>{message}</p>"
    from_email = "kishanpadhi291@gmail.com"
    to_email = to_email

    email = EmailMessage(subject, body, from_email, to_email)
    email.content_subtype = "html"  # Set the content type as HTML

    try:
        email.send()
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return False

class IssueCRUDVIEW(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def post(self,request):
        project = Project.objects.filter(key=request.data["project"]).values("id").first()
        lastIndex = Issue.objects.filter(project_id=project["id"],status=int(request.data["status"])).order_by('-index').values("index").first()
        data = {
            "project": project["id"],
            "issue_type": int(request.data["issueType"]),
            "issue_description": request.data["description"],
            "status": int(request.data.get("status")),
            "priority": int(request.data["priority"]),
            "issue_summary": request.data["summary"],
            "assignee": request.data["assignee"],
            "reporter": request.data["reporter"],
            "index": 0,
            "updated_date": datetime.datetime.now()
        }
        serializer = IssueCRUDSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            lastCreatedIssue = Issue.objects.order_by('-created_date').values("id").first()
            attachments = list(request.FILES.values())
            for file in attachments:
                data = {
                    "issue_id": lastCreatedIssue["id"],
                    "attachment_file":file
                }
                serializer = AttachmentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({"error": "Something went wrong"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"created": "issue Created successfully."}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({"error": "Something went wrong"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        issue = Issue.objects.filter(pk=pk).delete()
        return Response({"success": "Issue Deleted Successfully"}, status=status.HTTP_200_OK)

class UpdateIssueFields(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_name(self,email):
        user = User.objects.filter(email=email).values("fullName").first()
        return user['fullName']

    def get(self,request,issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
            serializer = IssueSerializer(issue)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            return Response({"error": serializer.errors}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, issue_id):
        message = ""
        subject = ""
        try:
            issue = Issue.objects.get(pk=issue_id)
            subject = f"Issue of {issue.project.key} has Been Updated"
        except Issue.DoesNotExist:
            return Response({"error": "Issue not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.data["field"] == 'status':
            try:
                status_obj = Status.objects.get(pk=int(request.data["value"]))
                message = f"{self.get_user_name(request.user)} has changed Status of issue {issue.project.key}-" \
                          f"{issue.id} to " \
                          f"{issue.status} to {status_obj}"
            except Status.DoesNotExist:
                return Response({"error": "Status not found."}, status=status.HTTP_404_NOT_FOUND)
            issue.status = status_obj
        elif request.data["field"] == 'priority':
            try:
                priority_obj = Priority.objects.get(pk=int(request.data["value"]))
            except Priority.DoesNotExist:
                return Response({"error": "Priority not found."}, status=status.HTTP_404_NOT_FOUND)
            message = f"{self.get_user_name(request.user)} has changed Priority of issue {issue.project.key}-" \
                      f"{issue.id} to " \
                      f"{issue.priority} to {priority_obj}"
            issue.priority = priority_obj

        elif request.data["field"] == 'assignee':
            try:
                assignee_obj = User.objects.get(pk=request.data["value"])
            except User.DoesNotExist:
                return Response({"error": "Assignee not found."}, status=status.HTTP_404_NOT_FOUND)
            message = f"{self.get_user_name(request.user)} has changed Assignee of issue {issue.project.key}-" \
                      f"{issue.id}, From " \
                      f"{self.get_user_name(issue.assignee)} to {self.get_user_name(assignee_obj)}"
            issue.assignee = assignee_obj

        elif request.data["field"] == 'reporter':
            try:
                reporter_obj = User.objects.get(pk=request.data["value"])
            except User.DoesNotExist:
                return Response({"error": "Reporter not found."}, status=status.HTTP_404_NOT_FOUND)
            message = f"{self.get_user_name(request.user)} has changed Assignee of issue {issue.project.key}-" \
                      f"{issue.id}, From " \
                      f"{self.get_user_name(issue.reporter)} to {self.get_user_name(reporter_obj)}"
            issue.reporter = reporter_obj

        elif request.data["field"] == 'issue_type_id':
            try:
                issue_type_obj = IssueType.objects.get(pk=int(request.data["value"]))
            except IssueType.DoesNotExist:
                return Response({"error": "Issue Type not found."}, status=status.HTTP_404_NOT_FOUND)
            message = f"{self.get_user_name(request.user)} has changed Assignee of issue {issue.project.key}-" \
                      f"{issue.id}, From " \
                      f"{issue.issue_type} to {issue_type_obj}"
            issue.issue_type = issue_type_obj

        else:
            setattr(issue, request.data["field"], request.data["value"])
            message = f"{self.get_user_name(request.user)} has changed Assignee of issue {issue.project.key}-" \
                      f"{issue.id}, From " \
                      f"\"{issue.issue_summary}\" to {request.data['value']}"
        issue.updated_date = datetime.datetime.now()
        issue.save()

        teamArr = list()
        team = TeamEmailAddress(Team.objects.filter(project_id=issue.project.id),many=True)
        to_email = list()
        for team in team.data:
            teamArr.append(team["email"])
        for team in teamArr:
            to_email.append(team["email"])
        # data = send_email(subject,message,to_email)
        return Response({"message": "Fields updated successfully."},status=status.HTTP_200_OK)

class PostCommentIssue(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,issue_id):
        print(issue_id)
        comment = Comment.objects.filter(issue_id=issue_id)
        serializer = CommentSerializer(comment,many=True)
        return Response({'success': serializer.data}, status=status.HTTP_200_OK)

    def post(self,request):
        data = {
            "comment_text":request.data['comment_text'],
            "user_id":request.data['user_id'],
            "issue_id":int(request.data['issue_id']),
        }
        print(data)
        serializer = CreateCommentatorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            comment = Comment.objects.filter(issue_id=int(request.data['issue_id']),user_id=request.data['user_id']).last()
            lastcomment = CommentSerializer(comment)
            return Response({'lastcomment':lastcomment.data},status=status.HTTP_200_OK)
        else:
            return Response({'Error':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk):
        comment = Comment.objects.filter(pk=pk).delete()
        return Response({"success":"Comment deleted successfully"})

    def patch(self,request,pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        comment.comment_text = request.data["comment_text"]
        comment.save()
        return Response({"success": "Comment Updated successfully"})

class UploadCsvIssues(APIView):

    def post(self, request):
        file = request.FILES.get('file')
        df = pd.read_csv(file)
        data_list = df.to_dict(orient='records')
        serializer = IssueImportSerializer(data=data_list, many=True)
        if serializer.is_valid():
            serializer.save()
            print('done')
            return Response({"success": "Data imported successfully"})
        else:
            return Response({"errors": serializer.errors})

        # return Response({"success": "Data imported successfully"})
        # df = pd.read_csv(file)
        # data_list = df.to_dict(orient='records')
        # serializer = IssueImportSerializer(data=data_list,many=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"success": "Data imported successfully"})
        # else:
        #     return Response({"errors": serializer.errors})

class IssueFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        searchText = request.data["search"]
        keys = request.data["keys"]
        user = request.data["user"]
        issue_type = request.data["type"]

        if len(searchText) != 0 and len(user) != 0 and len(issue_type) != 0:
            user_list = [x for x in user.split(',')]
            type_list = [int(x) for x in issue_type.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(issue_type_id__in=type_list) &
                                          Q(assignee_id__in=user_list) &
                                          Q(issue_summary__icontains=searchText))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        elif len(user) != 0 and len(issue_type) != 0:
            user_list = [x for x in user.split(',')]
            type_list = [int(x) for x in issue_type.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(issue_type_id__in=type_list) &
                                          Q(assignee_id__in=user_list))
            serializer = ProjectIssueSerializer(issues, many=True)
            return Response({"data": serializer.data})
        elif len(searchText) != 0 and len(issue_type) != 0:
            type_list = [int(x) for x in issue_type.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(issue_type_id__in=type_list) &
                                          Q(issue_summary__icontains=searchText))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        elif len(searchText) != 0 and len(user) != 0:
            user_list = [x for x in user.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(assignee_id__in=user_list) &
                                          Q(issue_summary__icontains=searchText))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        elif len(searchText):
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(issue_summary__icontains=searchText))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        elif len(issue_type) != 0:
            type_list = [int(x) for x in issue_type.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(issue_type_id__in=type_list))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        elif len(user) != 0:
            user_list = [x for x in user.split(',')]
            issues = Issue.objects.filter(Q(project__key=keys) &
                                          Q(assignee_id__in=user_list))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})
        else:
            issues = Issue.objects.filter(Q(project__key=keys))
            serializer = ProjectIssueSerializer(issues,many=True)
            return Response({"data": serializer.data})