from django.db import models
from Users.models import User



class Tasks(models.Model):

    class TaskStatus(models.TextChoices):
        PENDING = 'PEN'
        COMPLETED = 'COM'
        EXPIRED = 'EXP'


    status = models.CharField(
        max_length=3, 
        choices=TaskStatus.choices, 
        default=TaskStatus.PENDING
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='User_Tasks'
    )

    title = models.CharField(max_length=255)
    # New unique field for Accsessing the entire task
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dead_line = models.DateTimeField()


    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    

    def __str__(self):
        return self.title