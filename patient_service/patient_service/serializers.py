from rest_framework import serializers
from .models import Patient, Fullname, Category, RegularPatient, VIPPatient, EmergencyPatient

class FullnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fullname
        fields = ['first_name', 'middle_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class RegularPatientSerializer(CategorySerializer):
    class Meta:
        model = RegularPatient
        fields = ['name', 'insurance_number']

class VIPPatientSerializer(CategorySerializer):
    class Meta:
        model = VIPPatient
        fields = ['name', 'membership_level', 'dedicated_support']

class EmergencyPatientSerializer(CategorySerializer):
    class Meta:
        model = EmergencyPatient
        fields = ['name', 'emergency_level', 'admitted_at']

class PatientSerializer(serializers.ModelSerializer):
    fullname = FullnameSerializer()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'fullname', 'category', 'age', 'medical_history', 'created_at', 'updated_at']

    def get_category(self, obj):
        category = obj.category
        if isinstance(category, RegularPatient):
            return RegularPatientSerializer(category).data
        elif isinstance(category, VIPPatient):
            return VIPPatientSerializer(category).data
        elif isinstance(category, EmergencyPatient):
            return EmergencyPatientSerializer(category).data
        return CategorySerializer(category).data

    def create(self, validated_data):
        fullname_data = validated_data.pop('fullname')
        category_data = validated_data.pop('category')
        fullname = Fullname.objects.create(**fullname_data)

        # Tạo category dựa trên loại bệnh nhân
        category_type = category_data.get('type', 'regular')
        if category_type == 'regular':
            category = RegularPatient.objects.create(name=category_data['name'], insurance_number=category_data.get('insurance_number'))
        elif category_type == 'vip':
            category = VIPPatient.objects.create(name=category_data['name'], membership_level=category_data.get('membership_level'), dedicated_support=category_data.get('dedicated_support'))
        elif category_type == 'emergency':
            category = EmergencyPatient.objects.create(name=category_data['name'], emergency_level=category_data.get('emergency_level'))
        else:
            raise serializers.ValidationError("Invalid category type")

        patient = Patient.objects.create(fullname=fullname, category=category, **validated_data)
        return patient