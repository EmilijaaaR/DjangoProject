from rest_framework import serializers
from tasks.models.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'owner']
        read_only_fields = ['id', 'owner']