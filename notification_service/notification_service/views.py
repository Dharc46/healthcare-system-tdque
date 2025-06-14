from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, NotificationLog
from .serializers import NotificationSerializer, NotificationLogSerializer
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

class Notify(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            
            # Xử lý gửi thông báo (giả lập email/SMS/push)
            try:
                if notification.notification_type == 'email':
                    self.send_email(notification)
                elif notification.notification_type == 'sms':
                    self.send_sms(notification)
                elif notification.notification_type == 'push':
                    self.send_push(notification)
                
                notification.status = 'sent'
                NotificationLog.objects.create(
                    notification=notification,
                    status='success'
                )
            except Exception as e:
                notification.status = 'failed'
                NotificationLog.objects.create(
                    notification=notification,
                    status='failed',
                    error_message=str(e)
                )
            notification.save()
            
            return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, notification):
        # Giả lập gửi email
        msg = MIMEText(notification.message)
        msg['Subject'] = 'Healthcare Notification'
        msg['From'] = settings.EMAIL_SENDER
        msg['To'] = f"user_{notification.recipient_id}@example.com"  # Giả lập email recipient
        
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
    
    def send_sms(self, notification):
        # Giả lập gửi SMS (có thể tích hợp với Twilio hoặc dịch vụ SMS khác)
        pass
    
    def send_push(self, notification):
        # Giả lập gửi push notification (có thể tích hợp với Firebase hoặc OneSignal)
        pass

class NotificationHistory(APIView):
    def get(self, request, recipient_id):
        notifications = Notification.objects.filter(recipient_id=recipient_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)