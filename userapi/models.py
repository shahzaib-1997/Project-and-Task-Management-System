from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    add_members = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.project} - {self.user}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
    due_date = models.DateField()
    deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
