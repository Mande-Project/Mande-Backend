from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('list_filter_user/<str:user>/', NotificationViewSet.as_view({'get':'list_filter_user'}), name='list_filter_user')
]

#urlpatterns = router.urls