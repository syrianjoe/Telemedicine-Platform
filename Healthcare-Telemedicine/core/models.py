from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Patient(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    blood_type = models.CharField(max_length=3, blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Patient"

# MAKE SURE THIS CLASS IS PRESENT AND SPELLED EXACTLY LIKE THIS:
class Doctor(TimeStampedModel):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('general', 'General Practice'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50)
    years_of_experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.last_name} - {self.get_specialization_display()}"

class Appointment(TimeStampedModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'), 
        ('confirmed', 'Confirmed'), 
        ('completed', 'Completed'), 
        ('cancelled', 'Cancelled')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)

class HealthRecord(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    weight = models.FloatField(validators=[MinValueValidator(0)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    blood_pressure = models.CharField(max_length=10, blank=True, help_text="e.g., 120/80") # Add this line
    notes = models.TextField(blank=True)

class ChatHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, default='general')