from django.urls import path
from .views import TaskViewSet, TaskListViewSet, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView

app_name = 'task'

urlpatterns = [
    # API endpoints
    path('api/tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task_api_list_create'),
    path('api/tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task_api_retrieve-update-destroy'),

    # Template views
    path('tasks/', TaskListViewSet.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
