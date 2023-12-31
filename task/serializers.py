from django.contrib.auth.models import User
from rest_framework import serializers
from .models import  Task, Photo, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PhotoSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer()  # Represent the User who uploaded the photo

    class Meta:
        model = Photo
        fields = ('id', 'image', 'uploaded_by')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at')

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embed UserSerializer in TaskSerializer
    photos = PhotoSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'status', 'created_at', 'updated_at', 'user', 'photos', 'comments')
