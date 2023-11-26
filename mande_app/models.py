from django.db import models
from users.models import Worker, Customer

# Create your models here.
class Job(models.Model):
    name=models.CharField(max_length=255)

class Worker_Job(models.Model):
    worker=models.OneToOneField(Worker,on_delete=models.CASCADE)
    job=models.OneToOneField(Job,on_delete=models.CASCADE)
    price=models.FloatField()
    description=models.TextField()

class Service(models.Model):
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE)
    worker_job=models.OneToOneField(Worker_Job,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.BooleanField(default=False)
    hours=models.IntegerField()
    cost=models.FloatField()
    rating=models.FloatField(null=True)
    description=models.TextField()
