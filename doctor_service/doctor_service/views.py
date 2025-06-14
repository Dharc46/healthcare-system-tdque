from rest_framework.views import APIView 
from rest_framework.response import Response 
 
DOCTOR_DB = { 
    1: {"name": "Dr. John", "specialty": "Cardiology"}, 
    2: {"name": "Dr. Jane", "specialty": "Pediatrics"}, 
} 
 
class DoctorDetail(APIView): 
    def get(self, request, doctor_id): 
        doctor = DOCTOR_DB.get(doctor_id) 
        if doctor: 
            return Response(doctor) 
        return Response({"error": "Doctor not found"}, status=404) 
