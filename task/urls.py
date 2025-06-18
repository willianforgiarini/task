from django.urls import path, include
from .views import TaskViewSet, AuditoriaListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename="tasks")

urlpatterns = [
    path('', include(router.urls)),
    path("auditoria/", AuditoriaListView.as_view(), name="auditoria")
]
