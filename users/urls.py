from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import routers  
from .views import *

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('users/',CustomUserViewSet.as_view({'post':'create','delete':'destroy'}),name="user_view"),
    path('users/me/',CustomUserViewSet.as_view({'get':'retrieve', 'patch':'partial_update','delete':'destroy','put':'update'}),name="user_view"),
    path('customer/', CustomerViewSet.as_view()),
    path('worker/', WorkerViewSet.as_view()),
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]