from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Patient, Doctor, Appointment, HealthRecord
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample doctors
        doctors_data = [
            {'username': 'dr_smith', 'first_name': 'John', 'last_name': 'Smith', 
             'specialization': 'cardiology', 'license': 'MD12345', 'fee': 150, 'experience': 12},
            {'username': 'dr_jones', 'first_name': 'Sarah', 'last_name': 'Jones', 
             'specialization': 'dermatology', 'license': 'MD67890', 'fee': 120, 'experience': 8},
            {'username': 'dr_wong', 'first_name': 'Michael', 'last_name': 'Wong', 
             'specialization': 'pediatrics', 'license': 'MD54321', 'fee': 100, 'experience': 15},
        ]
        
        for doc_data in doctors_data:
            user, created = User.objects.get_or_create(
                username=doc_data['username'],
                defaults={
                    'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name'],
                    'email': f"{doc_data['username']}@hospital.com",
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': doc_data['specialization'],
                    'license_number': doc_data['license'],
                    'years_of_experience': doc_data['experience'],
                    'consultation_fee': doc_data['fee'],
                    'bio': f"Experienced {doc_data['specialization']} specialist with {doc_data['experience']} years of practice."
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('📝 Test credentials:'))
        self.stdout.write(self.style.SUCCESS('   Doctors: dr_smith / password123'))
        self.stdout.write(self.style.SUCCESS('   Register new patients via the website'))