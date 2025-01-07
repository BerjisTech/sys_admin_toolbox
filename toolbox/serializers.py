from rest_framework import serializers
from .models import Category, Tool, Server, ServerLog

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'

class ServerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerLog
        fields = '__all__'

class ServerSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    logs = ServerLogSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=Category.objects.all(), write_only=True
    )
    tools = ToolSerializer(many=True, read_only=True)
    tool_ids = serializers.PrimaryKeyRelatedField(
        source='tools', many=True, queryset=Tool.objects.all(), write_only=True
    )

    class Meta:
        model = Server
        fields = [
            'id', 'parent', 'name', 'description', 'category', 'category_id',
            'ip_address', 'endpoint', 'tools', 'tool_ids', 'children',
            'logs', 'created_at'
        ]
