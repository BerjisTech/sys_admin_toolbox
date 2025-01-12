from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ToolViewSet, ServerViewSet, ServerLogViewSet, system_metrics, check_uptime, docker_logs

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tools', ToolViewSet, basename='tool')
router.register(r'servers', ServerViewSet, basename='server')
router.register(r'logs', ServerLogViewSet, basename='serverlog')

urlpatterns = [
    path('', include(router.urls)),
    path('system-metrics/', system_metrics, name='system-metrics'),
    path('check-uptime/<int:server_id>/', check_uptime, name='check-uptime'),
    path('docker-logs/<str:container_name>/', docker_logs, name='docker-logs'),
]
