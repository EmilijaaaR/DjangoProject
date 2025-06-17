from rest_framework import generics, permissions
from tasks.models.Models import Task
from tasks.serializers.serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Vraća samo taskove vlasnika (ulogovanog korisnika)
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Vraća samo taskove vlasnika
        return Task.objects.filter(owner=self.request.user)