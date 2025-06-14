from django.urls import path 
from .views import ViewRecord 
urlpatterns = [ 
path('record/<int:patient_id>/', ViewRecord.as_view(), name='view-record'), 
] 