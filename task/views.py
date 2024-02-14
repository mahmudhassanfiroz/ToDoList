
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.views.generic import TemplateView, DetailView
from .models import Task, Photo
from .serializers import TaskSerializer, PhotoSerializer
from .forms import TaskForm, PhotoForm
from django.views.generic.edit import FormView
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.views import View
from django.http import HttpResponse



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

        search_keyword = self.request.GET.get('search')
        if search_keyword:
            tasks = tasks.filter(title__icontains=search_keyword)

        due_date = self.request.GET.get('due_date')
        if due_date:
            tasks = tasks.filter(due_date__lte=due_date)

        priority = self.request.GET.get('priority')
        if priority:
            tasks = tasks.filter(priority=priority)

        completed = self.request.GET.get('completed')
        if completed is not None:
            if completed.lower() == 'true':
                tasks = tasks.filter(completed=True)
            else:
                tasks = tasks.filter(completed=False)

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
class TaskCreateView(FormView):
    template_name = 'task/task_create.html'
    form_class = TaskForm
    success_url = ('/tasks/')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()

        # Process the photo form
        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.task = task
            photo.uploaded_by = self.request.user
            photo.save()

        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)
# TCRUD Views with Templates Update 
class TaskUpdateView(DetailView):
    model = Task
    template_name = 'task/task_update.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TaskForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task:task_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

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
        messages.success(request, 'Task deleted successfully.')
        return redirect('task:task_list')

# DetailView with Template
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        photos = Photo.objects.filter(task=task)
        context['photos'] = photos
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.task = task
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully.')
            return redirect('task:task_detail', pk=task.pk)  # Pass pk argument here
        else:
            return render(request, self.template_name, {'task': task, 'photo_form': photo_form})
class MyView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES['image']

        # Image resize
        img = Image.open(image)
        img = img.resize((200, 200))
        img.save('resized_image.jpg')

        # Image crop
        img = Image.open(image)
        img = img.crop((0, 0, 100, 100))
        img.save('cropped_image.jpg')

        # Thumbnail creation
        img = Image.open(image)
        img.thumbnail((100, 100))
        img.save('thumbnail.jpg')

        # Add watermark
        img = Image.open(image)
        watermark = Image.open('watermark.png')
        img.paste(watermark, (0, 0))
        img.save('watermarked_image.jpg')

        return HttpResponse('Image processed successfully!')


class PhotoUploadView(FormView):
    template_name = 'task/upload_photos.html'
    form_class = PhotoForm

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs['pk']
        context['task'] = Task.objects.get(pk=task_id)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            task_id = self.kwargs['pk']
            task = Task.objects.get(pk=task_id)
            images = self.request.FILES.getlist('images')
            for image in images:
                photo = Photo(task=task, uploaded_by=self.request.user)
                photo.image = self.process_uploaded_image(image)
                photo.save()
            return redirect('task:task_detail', pk=task.pk)
        else:
            return self.form_invalid(form)

    def process_uploaded_image(self, image):
        img = Image.open(image)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.thumbnail((300, 300))
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        file = InMemoryUploadedFile(
            buffer,
            None,
            image.name,
            'image/jpeg',
            buffer.tell(),
            None
        )
        return file

class PhotoDeleteView(View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        if request.method == 'POST':
            photo.delete()
            return HttpResponseRedirect(reverse('task:task_detail', kwargs={'pk': photo.task.pk}))
        else:
            return HttpResponseRedirect(reverse('task:task_detail', kwargs={'pk': photo.task.pk}))
