from django.contrib import admin
from .models import Service, Job, Worker_Job

admin.site.register(Service)
admin.site.register(Job)
admin.site.register(Worker_Job)
