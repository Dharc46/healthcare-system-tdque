from django.urls import path 
from .views import ViewRecord 

urlpatterns = [
    path('records/', ViewRecord.as_view(), name='view-record'),
]