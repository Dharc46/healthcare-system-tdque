from rest_framework import serializers
from .models import Notification, NotificationLog

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient_id', 'recipient_type', 'message', 'notification_type', 'status', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data['notification_type'] not in ['email', 'sms', 'push']:
            raise serializers.ValidationError("Invalid notification type")
        if data['recipient_type'] not in ['patient', 'doctor']:
            raise serializers.ValidationError("Invalid recipient type")
        return data

class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ['id', 'notification', 'status', 'error_message', 'sent_at']