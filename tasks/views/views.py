from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models.Models import Task
from tasks.serializers.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import extend_schema_view
from tasks.serializers.serializers import TaskBatchUpdateSerializer, TaskBatchDeleteSerializer


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'due_date', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']
    ordering = ['priority']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='search', type=str, description='Search title or description'),
            OpenApiParameter(name='ordering', type=str, description='Sort by priority, due_date, etc.'),
            OpenApiParameter(name='status', type=int),
            OpenApiParameter(name='category', type=int),
            OpenApiParameter(name='priority', type=str),
            OpenApiParameter(name='due_date', type=str),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskBatchUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=TaskBatchUpdateSerializer,
        responses={200: None},
    )
    def put(self, request):
        updates = request.data.get('updates', [])

        for item in updates:
            try:
                task = Task.objects.get(uid=item['uid'], owner=request.user)
                for key, value in item.items():
                    if key != 'uid':
                        setattr(task, key, value)
                task.save()
            except Task.DoesNotExist:
                continue

        return Response({"message": "Tasks updated."}, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        request=TaskBatchDeleteSerializer,
        responses={200: None},
    )
)
class TaskBatchDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        serializer = TaskBatchDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']

        Task.objects.filter(uid__in=ids, owner=request.user).delete()

        return Response({"message": "Tasks deleted."}, status=status.HTTP_200_OK)
