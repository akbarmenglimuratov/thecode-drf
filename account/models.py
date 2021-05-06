from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    verified = models.BooleanField(default = False)
    date_of_birth = models.DateField(blank=True, null=True)
    reputation = models.IntegerField(default = 0)
