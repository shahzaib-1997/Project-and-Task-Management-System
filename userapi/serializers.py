from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "members"]


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "project",
        ]
