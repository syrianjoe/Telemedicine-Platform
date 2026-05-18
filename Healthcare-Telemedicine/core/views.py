from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Patient, Appointment, HealthRecord

def home(request):
    """View function for the platform landing/home page."""
    return render(request, 'core/home.html')

def register(request):
    """View function handling new user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Establish matching Patient profile link
            Patient.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')[:5]
        health_records = HealthRecord.objects.filter(patient=patient).order_by('-created_at')[:5]

        stats = {
            'total_appointments': appointments.count(),
            'upcoming_appointments': appointments.filter(status__in=['scheduled', 'confirmed']).count(),
            'health_records_count': HealthRecord.objects.filter(patient=patient).count(),
            'last_heart_rate': health_records.first().heart_rate if health_records.exists() else "--"
        }
    except Patient.DoesNotExist:
        appointments, health_records, stats = [], [], {}

    return render(request, 'core/dashboard.html', {
        'appointments': appointments,
        'health_records': health_records,
        'stats': stats
    })