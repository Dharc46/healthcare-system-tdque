from django.db import models

class ChatQuery(models.Model):
    user_id = models.IntegerField()  # ID người dùng
    query_text = models.TextField(blank=True, null=True)  # Câu hỏi văn bản
    symptoms = models.JSONField(blank=True, null=True)  # Danh sách triệu chứng (JSON)
    predicted_disease = models.CharField(max_length=50, blank=True, null=True)  # Bệnh dự đoán
    response = models.TextField()  # Phản hồi chatbot
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by user {self.user_id}: {self.query_text or self.symptoms}"