# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectAPIView, TaskAPIView, UserViewSet, home

router = DefaultRouter()
router.register(r'auth', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', home, name='home'),
    path('project/', ProjectAPIView.as_view(), name="projects"),
    path('project/<int:pk>/', ProjectAPIView.as_view(), name="projects"),
    path('task/', TaskAPIView.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskAPIView.as_view(), name="tasks")
]
