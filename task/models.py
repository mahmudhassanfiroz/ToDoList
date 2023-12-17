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
  completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

  def __str__(self):
    return self.title

# Photo Model
class Photo(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='photos')
  image = models.ImageField(upload_to="task_photos", blank=True)

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
  
