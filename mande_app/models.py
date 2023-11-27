from django.db import models
from users.models import Worker, Customer

# Create your models here.
class Job(models.Model):
    name=models.CharField(max_length=255)

class Worker_Job(models.Model):
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    price=models.FloatField()
    description=models.TextField()

class Service(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    worker_job=models.ForeignKey(Worker_Job,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.BooleanField(default=False)
    hours=models.IntegerField()
    cost=models.FloatField()
    rating=models.FloatField(null=True)
    description=models.TextField()
