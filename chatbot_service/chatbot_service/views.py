import json
import re
import numpy as np
import markdown
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import ChatQuery
from .serializers import ChatQuerySerializer
from .ml_model import model, predict_with_uncertainty, diseases, test_map, medicine_map

class ChatbotQuery(APIView):
    def load_knowledge_base(self):
        # Đọc knowledge base từ file Markdown
        with open('/app/knowledge_base_respiratory_diseases.markdown', 'r', encoding='utf-8') as file:
            return file.read()

    def extract_info_from_knowledge_base(self, query, knowledge_base):
        # Chuyển Markdown thành text thuần
        text = markdown.markdown(knowledge_base)
        
        # Tìm kiếm bệnh liên quan trong câu hỏi
        diseases = ["Cảm cúm thông thường", "Cúm", "Viêm phổi do virus", "Viêm xoang cấp tính"]
        disease_match = None
        for disease in diseases:
            if disease.lower() in query.lower():
                disease_match = disease
                break
        
        if not disease_match:
            return "Không tìm thấy thông tin phù hợp. Vui lòng cung cấp thêm chi tiết hoặc danh sách triệu chứng."

        # Tìm kiếm phần nội dung liên quan trong knowledge base
        pattern = rf'##\s*\d+\.\s*{disease_match}(.*?)(?=\n##\s*\d+\.|\Z)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return f"Thông tin về {disease_match} không đầy đủ. Vui lòng thử lại."

    def check_severe_symptoms(self, symptoms):
        # Kiểm tra triệu chứng nghiêm trọng từ knowledge base
        severe_symptoms = [
            "sốt cao", "khó thở", "đau ngực", "lú lẫn", "sưng mắt", "thay đổi thị lực",
            "tím tái môi", "co giật", "mê sảng", "hạ thân nhiệt"
        ]
        return any(symptom.lower() in symptoms.lower() for symptom in severe_symptoms)

    def send_notification(self, user_id, message):
        # Gửi thông báo qua NotificationService
        try:
            response = requests.post(
                'http://notification-service:8000/notify/',
                json={
                    "recipient_id": user_id,
                    "recipient_type": "patient",
                    "message": message,
                    "notification_type": "email"
                }
            )
            return response.status_code == 201
        except requests.RequestException:
            return False

    def post(self, request):
        serializer = ChatQuerySerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            query_text = serializer.validated_data.get('query_text', '')
            symptoms = serializer.validated_data.get('symptoms', [])
            
            # Khởi tạo diagnosis với giá trị mặc định
            diagnosis = None
            response_text = ""

            # Kiểm tra triệu chứng nghiêm trọng
            if query_text and self.check_severe_symptoms(query_text):
                self.send_notification(user_id, "Bạn có triệu chứng nghiêm trọng. Vui lòng đến bác sĩ ngay!")
                response_text = "Cảnh báo: Triệu chứng của bạn có thể nghiêm trọng. Hãy đến cơ sở y tế ngay lập tức."
            elif symptoms:
                # Dự đoán bệnh bằng mô hình ML
                symptom_names = ["Fever", "Cough", "Sneezing", "Fatigue", "Loss of Taste", "Itchy Eyes"]
                input_symptoms = [1 if s in symptoms else 0 for s in symptom_names]
                input_array = np.array([input_symptoms], dtype=np.float32)
                mean_probs, std_probs = predict_with_uncertainty(model, input_array)
                most_likely = np.argmax(mean_probs)
                diagnosis = diseases[most_likely]
                
                # Lấy thông tin từ knowledge base
                knowledge_base = self.load_knowledge_base()
                disease_info = self.extract_info_from_knowledge_base(diagnosis, knowledge_base)
                
                # Tạo phản hồi
                response_text = (
                    f"**Chẩn đoán**: Bạn có khả năng mắc {diagnosis} (xác suất: {mean_probs[0][most_likely]:.3f}, "
                    f"độ không chắc chắn: {std_probs[0][most_likely]:.3f}).\n"
                    f"**Xét nghiệm khuyến nghị**: {test_map[diagnosis]}.\n"
                    f"**Thuốc/Điều trị khuyến nghị**: {medicine_map[diagnosis]}.\n"
                    f"**Thông tin chi tiết**:\n{disease_info}"
                )
                
                # Kiểm tra triệu chứng nghiêm trọng trong input
                if self.check_severe_symptoms(json.dumps(symptoms)):
                    self.send_notification(user_id, "Bạn có triệu chứng nghiêm trọng. Vui lòng đến bác sĩ ngay!")
                    response_text += "\nCảnh báo: Triệu chứng của bạn có thể nghiêm trọng. Hãy đến cơ sở y tế ngay lập tức."
            else:
                # Trả lời câu hỏi văn bản
                knowledge_base = self.load_knowledge_base()
                response_text = self.extract_info_from_knowledge_base(query_text, knowledge_base)

            # Lưu truy vấn
            chat_query = serializer.save(
                predicted_disease=diagnosis, 
                response=response_text
            )
            
            # Tạo phản hồi JSON với UTF-8
            response_data = ChatQuerySerializer(chat_query).data
            response_json = json.dumps(response_data, ensure_ascii=False)  # Không escape ký tự Unicode
            return HttpResponse(
                content=response_json,
                content_type='application/json; charset=utf-8',  # Chỉ định charset=utf-8
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)