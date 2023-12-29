from django.contrib import admin
from .models import Task, Photo, Comment

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'priority', 'completed', 'created_at', 'updated_at']
    list_filter = ['due_date', 'priority', 'completed']
    search_fields = ['title']

    def has_add_permission(self, request):
        return False  # Disable the ability to add tasks from the admin

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object being added
            obj.user = request.user  # Set the user to the current logged-in user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']

    def has_add_permission(self, request):
        return False  # Disable the ability to add comments from the admin

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object being added
            obj.user = request.user  # Set the user to the current logged-in user
        super().save_model(request, obj, form, change)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['task', 'image', 'uploaded_by']
    list_filter = ['uploaded_by']
    search_fields = ['image']

    def has_add_permission(self, request):
        return False  # Disable the ability to add photos from the admin

    def uploaded_by(self, obj):
        return obj.uploaded_by.username  # Display the username of the uploader

    uploaded_by.short_description = "Uploaded By"  # Set a custom header for the uploaded_by column
