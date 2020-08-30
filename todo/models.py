from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Todo(models.Model):

    task = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.task
