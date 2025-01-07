from django.shortcuts import render

# Create your views here.
import psutil
import requests
import docker
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Tool, Server, ServerLog
from .serializers import (
    CategorySerializer, ToolSerializer,
    ServerSerializer, ServerLogSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

class ServerLogViewSet(viewsets.ModelViewSet):
    queryset = ServerLog.objects.all()
    serializer_class = ServerLogSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

@api_view(['GET'])
def system_metrics(request):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    data = {
        "cpu_usage": cpu_usage,
        "memory_used": memory_info.used,
        "memory_percent": memory_info.percent,
        "total_memory": memory_info.total
    }
    return Response(data)

@api_view(['GET'])
def check_uptime(request, server_id):
    from .models import Server
    try:
        server = Server.objects.get(id=server_id)
    except Server.DoesNotExist:
        return Response({"error": "Server not found"}, status=404)

    url_to_check = server.endpoint
    if not url_to_check:
        return Response({"error": "Server has no endpoint"}, status=400)

    try:
        resp = requests.get(url_to_check, timeout=5)
        return Response({
            "server": server.name,
            "status_code": resp.status_code,
            "is_up": resp.status_code == 200
        })
    except requests.exceptions.RequestException as e:
        return Response({"server": server.name, "error": str(e)}, status=500)
    
@api_view(['GET'])
def docker_logs(request, container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=100)  # last 100 lines
        return Response({"container": container_name, "logs": logs.decode('utf-8')})
    except docker.errors.NotFound:
        return Response({"error": "Container not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)