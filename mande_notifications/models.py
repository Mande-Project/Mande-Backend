from django.db import models
from users.models import CustomUser

class Notification(models.Model):
    subject = models.TextField(max_length=50)
    body = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    as_customer = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

