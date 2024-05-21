from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='project_members', blank=True)
    

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    due_date = models.DateField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
