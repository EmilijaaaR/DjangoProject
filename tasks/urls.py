from django.urls import path
from tasks.views.views import TaskListView, TaskCreateView, TaskDetailView, TaskBatchDeleteView, TaskBatchUpdateView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<uuid:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/batch-update/', TaskBatchUpdateView.as_view(), name='task-batch-update'),
    path('tasks/batch-delete/', TaskBatchDeleteView.as_view(), name='task-batch-delete'),
]