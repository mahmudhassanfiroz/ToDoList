from django import forms
from .models import Task, Photo
from multiupload.fields import MultiFileField

class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed')])

    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'priority', 'status')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[('in_progress', 'In Progress'), ('completed', 'Completed')]),
        }

class PhotoForm(forms.ModelForm):
  
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
    image_size = forms.CharField(max_length=20, required=False, help_text='Enter size in WxH format (e.g., 300x300)')
    class Meta:
        model = Photo
        fields = ['image', 'image_size']



