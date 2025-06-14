from django.db import models
from django.core.exceptions import ValidationError

class Fullname(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    # By removing 'abstract = True', this becomes a concrete model
    # with its own database table.
    # class Meta:
    #     abstract = True

    def calculate_priority(self):
        raise NotImplementedError("Subclasses must implement calculate_priority")

class RegularPatient(Category):
    # This model will now have an implicit OneToOneField to the Category table.
    insurance_number = models.CharField(max_length=20, blank=True, null=True)

    def calculate_priority(self):
        return 1  # Priority: Low

    def __str__(self):
        return f"Regular: {self.name}"

class VIPPatient(Category):
    # This model will also have an implicit OneToOneField to the Category table.
    membership_level = models.CharField(max_length=20, choices=[('gold', 'Gold'), ('platinum', 'Platinum')])
    dedicated_support = models.BooleanField(default=True)

    def calculate_priority(self):
        return 3  # Priority: High

    def __str__(self):
        return f"VIP: {self.name}"

class EmergencyPatient(Category):
    # And so will this one.
    emergency_level = models.CharField(max_length=20, choices=[('critical', 'Critical'), ('urgent', 'Urgent')])
    admitted_at = models.DateTimeField(auto_now_add=True)

    def calculate_priority(self):
        return 5  # Priority: Highest

    def __str__(self):
        return f"Emergency: {self.name}"

class Patient(models.Model):
    fullname = models.OneToOneField(Fullname, on_delete=models.CASCADE)
    # This ForeignKey now correctly points to the concrete Category model.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    age = models.IntegerField()
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.age < 0:
            raise ValidationError("Age cannot be negative")

    def __str__(self):
        return f"{self.fullname} ({self.category})"
