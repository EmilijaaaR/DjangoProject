from rest_framework import serializers
from tasks.models.Models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'owner',
            'category', 'priority', 'status', 'due_date',
            'created_at', 'updated_at', 'parent'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_description(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("Description must be 255 characters or fewer.")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TaskUpdateItemSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    category = serializers.IntegerField(required=False)

class TaskBatchUpdateSerializer(serializers.Serializer):
    updates = TaskUpdateItemSerializer(many=True)

class TaskBatchDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.UUIDField(), 
        allow_empty=False
    )