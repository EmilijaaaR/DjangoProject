from django.db import models
from django.conf import settings
from django.utils.timezone import now
import uuid

class Task(models.Model):
    PRIORITY_CHOICES = [
    ('1', 'Low'),
    ('2', 'Medium'),
    ('3', 'High'),
]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    status = models.ForeignKey('TaskStatus', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    category = models.ForeignKey('TaskCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtasks')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        return self.due_date and self.due_date < now().date()

    def is_due_today(self):
        return self.due_date == now().date()

    def __str__(self):
        return self.title


class TaskCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    from django.db import models

class TaskStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name