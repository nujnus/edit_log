from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomizeUser(AbstractUser):
    #author = models.CharField(max_length=12)
    #login = models.BooleanField(default=False)

    def __str__(self):
        return self.username

