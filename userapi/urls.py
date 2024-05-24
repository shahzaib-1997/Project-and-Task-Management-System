# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectAPIView, TaskAPIView, UserViewSet, ProjectMemberAPIView

router = DefaultRouter()
router.register(r"auth", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("projects/", ProjectAPIView.as_view(), name="projects"),
    path("projects/<int:pk>/", ProjectAPIView.as_view(), name="projects"),
    path("projects/<int:project_id>/tasks/", TaskAPIView.as_view()),
    path("projects/<int:project_id>/tasks/<int:pk>/", TaskAPIView.as_view()),
    path("projects/<int:project_id>/members/", ProjectMemberAPIView.as_view()),
    path(
        "projects/<int:project_id>/members/<int:user_id>/",
        ProjectMemberAPIView.as_view(),
    ),
]
