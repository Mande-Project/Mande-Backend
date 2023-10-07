from django.urls import path, include, re_path
from rest_framework import routers
from .views import CustomUserViewSet
from django.views.generic import TemplateView  

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]

""" from .views import customer_register, customer_login, worker_register, worker_login,  user_logout

urlpatterns = [
    path('customer_register/', customer_register, name='customer_register'),
    path('customer_login/', customer_login, name='customer_login'),
    path('worker_register/', worker_register, name='worker_register'),
    path('worker_login/', worker_login, name='worker_login'),
    
    path('logout/', user_logout, name='user_logout'),
] """