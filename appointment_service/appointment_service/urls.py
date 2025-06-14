from django.urls import path 
from .views import MakeAppointment 
 
urlpatterns = [ 
    path('make/', MakeAppointment.as_view(), name='make-appointment'), 
]