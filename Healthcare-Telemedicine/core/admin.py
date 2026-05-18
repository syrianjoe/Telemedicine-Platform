from django.contrib import admin
from .models import Patient, Doctor, Appointment, HealthRecord, ChatHistory

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'blood_type', 'phone_number']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'years_of_experience', 'consultation_fee', 'available']
    list_filter = ['specialization', 'available']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_time', 'status']
    list_filter = ['status', 'date_time']
    search_fields = ['patient__user__first_name', 'doctor__user__last_name']

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'weight', 'blood_pressure', 'heart_rate', 'created_at']
    list_filter = ['created_at']

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_bot', 'message_type', 'created_at']
    list_filter = ['is_bot', 'message_type', 'created_at']
    search_fields = ['user__username', 'message']
