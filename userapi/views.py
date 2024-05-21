from datetime import timedelta
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.db.utils import IntegrityError
import jwt
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer
from .permissions import CRUDPermission


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
                "exp": timezone.now() + timedelta(hours=24),
                "iat": timezone.now(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return Response({"msg": "Login successfully!", "token": token})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectAPIView(views.APIView):
    permission_classes = [CRUDPermission]

    def get(self, request):
        try:
            projects = Project.objects.filter(
                deleted=False, owner=request.GET["user_id"]
            )
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
            data["owner"] = request.GET["user_id"]
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


class TaskAPIView(views.APIView):
    permission_classes = [CRUDPermission]

    def get(self, request):
        try:
            project_id = request.GET.get("project_id", None)
            if project_id:
                tasks = Task.objects.filter(deleted=False, project=project_id)
                if tasks:
                    serializer = TaskSerializer(tasks, many=True)
                    return Response(
                        {"data": serializer.data},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"msg": "Tasks not created yet against given project id."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Please provide project id to get task of that project."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            project_id = request.GET.get("project_id", None)
            if project_id:
                user = request.GET["user_id"]
                project = get_object_or_404(Project, id=project_id)
                serializer = ProjectSerializer(project)
                if (
                    user in serializer.data["members"]
                    or user == serializer.data["owner"]
                ):
                    data = request.data
                    data["project"] = project_id
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
                return Response(
                    {"error": "You are not member or owner of this project!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": "Please provide project id to create task in that project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk=None):
        try:
            if pk:
                task = get_object_or_404(Task, id=pk)
                project_id = task.project.id
                user = request.GET["user_id"]
                project = get_object_or_404(Project, id=project_id)
                serializer = ProjectSerializer(project)
                if (
                    user in serializer.data["members"]
                    or user == serializer.data["owner"]
                ):
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
                    {"error": "You are not member or owner of this project!"},
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

    def delete(self, request, pk=None):
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
