from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
from django.contrib.auth.models import User

# Create your models here.

# User Model
# class User(AbstractUser):
#     # Add custom fields and methods for your User model here
#   avatar = models.ImageField(upload_to='avatars', blank=True)

#   def __str__(self):
#     return self.username

# Task Model
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="low"
    )
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', default=None)

    def __str__(self):
        return self.title

    def get_photos(self):
        return self.photos.all()

    def mark_as_complete(self):
        self.completed = True
        self.save()

    def mark_as_incomplete(self):
        self.completed = False
        self.save()
# Photo Model

class Photo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for task {self.task.title}"


# Comment Model
class Comment(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.user.username} on task {self.task.title}"
  
