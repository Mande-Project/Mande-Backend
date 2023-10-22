from django.urls import path
from .views import login_test

urlpatterns = [
    path('', login_test, name='login_test'),
]
