from django.db import models

class Notification(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    recipient_id = models.IntegerField()  # ID của bệnh nhân hoặc bác sĩ
    recipient_type = models.CharField(max_length=20, choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, default='pending')  # pending, sent, failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.notification_type} to {self.recipient_type}:{self.recipient_id} - {self.message[:50]}"

class NotificationLog(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # success, failed
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log for {self.notification} - {self.status}"