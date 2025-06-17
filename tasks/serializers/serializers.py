from rest_framework import serializers
from tasks.models.Models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'owner']
        read_only_fields = ['id', 'owner']

    def validate_description(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("Description must be 255 characters or fewer.")
        return value
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value