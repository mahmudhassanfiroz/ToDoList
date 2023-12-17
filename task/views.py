
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.generic import TemplateView
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm


# ViewSets
class TaskViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

# ListView with Filtering and Search
class TaskListViewSet(ListCreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TaskSerializer

  def get_queryset(self):
    tasks = Task.objects.filter(user=self.request.user)

    # Search by title
    search_query = self.request.GET.get('search')
    if search_query:
      tasks = tasks.filter(title__icontains=search_query)

    # Filter by various criteria
    due_date = self.request.GET.get('due_date')
    if due_date:
      tasks = tasks.filter(due_date__lte=due_date)
    priority = self.request.GET.get('priority')
    if priority:
      tasks = tasks.filter(priority=priority)
    completed = self.request.GET.get('completed')
    if completed:
      tasks = tasks.filter(completed=completed)

    return tasks

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def list(self, request, *args, **kwargs):
    tasks = self.get_queryset()
    serializer = self.get_serializer(tasks, many=True)
    return render(request, 'task/task_list.html', {'tasks': serializer.data})

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# CRUD Views with Templates Create 
class TaskCreateView(TemplateView):
  template_name = 'task/task_create.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = TaskForm()  # Assuming you have a TaskForm for task creation
    return context

  def post(self, request, *args, **kwargs):
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.user = request.user
      task.save()
      return redirect('task:task_list')  # Redirect to the task list after successful creation
    else:
      return render(request, self.template_name, {'form': form})

# TCRUD Views with Templates Update 
class TaskUpdateView(TemplateView):
  template_name = 'task/task_update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    task_id = self.kwargs.get('pk')
    task = Task.objects.get(pk=task_id)
    context['form'] = TaskForm(instance=task)
    return context

  def post(self, request, *args, **kwargs):
    task_id = self.kwargs.get('pk')
    task = Task.objects.get(pk=task_id)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
      form.save()
      return redirect('task:task_detail', pk=task_id)
    else:
      return render(request, self.template_name, {'form': form, 'task': task})

# CRUD Views with Templates
class TaskDeleteView(TemplateView):
  template_name = 'task/task_delete.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    task_id = self.kwargs.get('pk')
    context['task'] = Task.objects.get(pk=task_id)
    return context

  def post(self, request, *args, **kwargs):
    task_id = self.kwargs.get('pk')
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('task:task_list')

# DetailView with Template
class TaskDetailView(TemplateView):
  template_name = 'task/task_detail.html'

  def get(self, request, pk, format=None):
    try:
      task = self.get_object(pk)
      return render(request, self.template_name, {'task': task})
    except Http404:
      # Handle the case where the task is not found
      messages.error(request, 'Task not found')
      return redirect('task:task_list')

  def get_object(self, pk):
    try:
      task = Task.objects.get(pk=pk)
      if task.user != self.request.user:
        raise Http404
      return task
    except Task.DoesNotExist:
      raise Http404