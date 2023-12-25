from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import NotificationView, NotificationReadView

router = SimpleRouter()
router.register('notification', NotificationView, basename='notification')

urlpatterns = [
    path('read/', NotificationReadView.as_view())
]
urlpatterns += router.urls
