from datetime import timedelta
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.conf import settings
from django.db.utils import IntegrityError
import jwt
from .models import Project, Task, ProjectMember
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    UserSerializer,
    ProjectMemberSerializer,
)
from .authentication import UserAuthentication
from .permissions import (
    CanAddMembers,
    CanCreateTask,
    CanDeleteTask,
    CanUpdateTask,
    IsProjectMember,
)


def home(request):
    return render(request, "home.html")


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"])
    def register(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            if not username or not password:
                return Response(
                    {"error": "Username and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.create_user(username=username, password=password)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"error": "Account already exists with given username!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def login(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailed("Invalid credentials")
            payload = {
                "id": user.id,
                "exp": (timezone.now() + timedelta(hours=24)).timestamp(),
                "iat": timezone.now().timestamp(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return Response({"msg": "Login successfully!", "token": token})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [UserAuthentication]

    def get(self, request):
        try:
            projects = Project.objects.filter(deleted=False, owner=request.user)
            serializer = ProjectSerializer(projects, many=True)
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            data = request.data
            data["owner"] = request.user.id
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Project created successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk=None):
        try:
            if pk:
                project = get_object_or_404(Project, id=pk)
                if project.owner != request.user:
                    return Response(
                        {"error": "Only owner can update the project."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                data = request.data
                serializer = ProjectSerializer(project, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "msg": "Project updated successfully",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"error": "Project id not provided in url."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk=None):
        try:
            if pk:
                project = get_object_or_404(Project, id=pk)
                if project.owner != request.user:
                    return Response(
                        {"error": "Only owner can delete the project."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not project.deleted:
                    project.deleted = True
                    project.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(
                    {"msg": "Project already deleted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Project id not provided in url."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectMemberAPIView(views.APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated, CanAddMembers]

    def get(self, request, project_id):
        try:
            project_members = ProjectMember.objects.filter(
                deleted=False, project=project_id
            )
            serializer = ProjectMemberSerializer(project_members, many=True)
            return Response(
                {"data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, project_id):
        try:
            project = get_object_or_404(Project, id=project_id)
            data = request.data
            data["project"] = project.id
            serializer = ProjectMemberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Member added successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, project_id, user_id):
        try:
            project_member = get_object_or_404(
                ProjectMember, project_id=project_id, user_id=user_id
            )
            data = request.data
            serializer = ProjectMemberSerializer(
                project_member, data=data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "msg": "Permissions updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, project_id, user_id):
        try:
            project_member = get_object_or_404(
                ProjectMember, project_id=project_id, user_id=user_id
            )
            if request.user == project_member.project.owner:
                if not project_member.deleted:
                    project_member.deleted = True
                    project_member.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(
                    {"msg": "Project Member already deleted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Only project owner can delete members!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskAPIView(views.APIView):
    authentication_classes = [UserAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission() for permission in [IsAuthenticated, CanCreateTask]]
        elif self.request.method in ["PUT", "PATCH"]:
            return [permission() for permission in [IsAuthenticated, CanUpdateTask]]
        elif self.request.method == "DELETE":
            return [permission() for permission in [IsAuthenticated, CanDeleteTask]]
        return [permission() for permission in [IsAuthenticated, IsProjectMember]]

    def get(self, request, project_id):
        try:
            tasks = Task.objects.filter(deleted=False, project=project_id)
            if tasks:
                serializer = TaskSerializer(tasks, many=True)
                return Response(
                    {"data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"msg": "No tasks created yet against given project id."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, project_id):
        try:
            user = request.user
            data = request.data
            data["project"] = project_id
            data["created_by"] = user.id
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "msg": "Task created successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, project_id, pk=None):
        try:
            if pk:
                task = get_object_or_404(Task, id=pk)
                data = request.data
                serializer = TaskSerializer(task, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "msg": "Task updated successfully",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"error": "Task id not provided in url."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, project_id, pk=None):
        try:
            if pk:
                task = get_object_or_404(Task, id=pk)
                if not task.deleted:
                    task.deleted = True
                    task.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(
                    {"msg": "Task already deleted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Task id not provided in url."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
