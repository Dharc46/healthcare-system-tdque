from django.urls import path
from .views import Notify, NotificationHistory

urlpatterns = [
    path('notify/', Notify.as_view(), name='notify'),
    path('history/<int:recipient_id>/', NotificationHistory.as_view(), name='notification-history'),
]