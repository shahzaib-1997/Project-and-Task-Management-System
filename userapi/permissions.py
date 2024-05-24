from rest_framework import permissions
from .models import ProjectMember, Project


class IsProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == user:
            return True
        return ProjectMember.objects.filter(user=user, project_id=project_id).exists()


class CanCreateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == user:
            return True
        member = ProjectMember.objects.filter(user=user, project_id=project_id).first()
        return member and member.can_create


class CanUpdateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False
        print(user)
        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == user:
            return True
        member = ProjectMember.objects.filter(user=user, project_id=project_id).first()
        return member and member.can_update


class CanDeleteTask(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == user:
            return True
        member = ProjectMember.objects.filter(user=user, project_id=project_id).first()
        return member and member.can_delete


class CanAddMembers(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == user:
            return True
        member = ProjectMember.objects.filter(user=user, project_id=project_id).first()
        return member and member.add_members
