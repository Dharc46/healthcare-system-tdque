from rest_framework import serializers
from .models import ChatQuery

class ChatQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatQuery
        fields = ['id', 'user_id', 'query_text', 'symptoms', 'predicted_disease', 'response', 'created_at']
        extra_kwargs = {
            'response': {'read_only': True},  # Thêm dòng này
            'predicted_disease': {'read_only': True}
        }

    def validate(self, data):
        if not data.get('query_text') and not data.get('symptoms'):
            raise serializers.ValidationError("Phải cung cấp ít nhất một câu hỏi hoặc danh sách triệu chứng.")
        return data