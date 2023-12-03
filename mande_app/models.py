from django.db import models
from users.models import Worker, Customer, CustomUser

# Create your models here.
class Job(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Worker_Job(models.Model):
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    price=models.FloatField()
    description=models.TextField()

    def __str__(self):
        return self.job.name + " - " + self.worker.user.first_name + " " + self.worker.user.last_name

class Service(models.Model):
    STATUS_TYPES = [
        ('A', 'Active'),
        ('F', 'Finished'),
        ('C', 'Canceled'),
    ]
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    worker_job=models.ForeignKey(Worker_Job,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(default='A',choices=STATUS_TYPES,max_length=1)
    hours=models.IntegerField()
    cost=models.FloatField()
    rating=models.FloatField(null=True)
    description=models.TextField()

    def __str__(self):
        return f"Client: {self.user.username} - Worker: {self.worker_job.worker.user.username}, Job: {self.worker_job.job.name}"