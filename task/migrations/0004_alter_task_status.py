# Generated by Django 5.0 on 2023-12-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='todo', max_length=20),
        ),
    ]
