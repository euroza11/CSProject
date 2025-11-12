from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=10)
    rank = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}, {self.point}"
