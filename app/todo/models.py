from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        """
        It will not create a model treated as base class
        """
        abstract = True

class Todo(BaseModel):
    todo_name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_todos')
    