from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers  
from .views import *


urlpatterns = [
    path("jobs/", JobsAPI.as_view()),
    path("worker_job/", Worker_JobAPI.as_view()),
    path("services/", ServiceAPI.as_view()),
    path('docs/', include_docs_urls(title='Mande API')),
]
