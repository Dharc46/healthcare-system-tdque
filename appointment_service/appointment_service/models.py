from django.db import models 
class Appointment(models.Model): 
    patient_id = models.IntegerField() 
    doctor_id = models.IntegerField() 
    date = models.DateTimeField()