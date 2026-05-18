from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .services import HealthcareChatGPT, BasicHealthcareBot
from core.models import ChatHistory
import os

@csrf_exempt
@login_required
def chatgpt_api(request):
    """Main ChatGPT API endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_message = data.get('message', '').strip()
            chat_type = data.get('type', 'general')
            
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            # Save user message to database
            ChatHistory.objects.create(
                user=request.user,
                message=user_message,
                is_bot=False,
                message_type=chat_type
            )
            
            # Check if OpenAI API key is available
            if not os.getenv('OPENAI_API_KEY'):
                # Use basic bot as fallback
                bot = BasicHealthcareBot()
                response_text = bot.get_response(user_message)
            else:
                # Use ChatGPT
                chatgpt_service = HealthcareChatGPT()
                
                # Get recent conversation history for context
                recent_chats = ChatHistory.objects.filter(
                    user=request.user
                ).order_by('-created_at')[:10]
                
                conversation_history = []
                for chat in reversed(recent_chats):
                    role = "assistant" if chat.is_bot else "user"
                    conversation_history.append({
                        "role": role,
                        "content": chat.message
                    })
                
                if any(word in user_message.lower() for word in ['symptom', 'pain', 'hurt', 'fever', 'headache']):
                    response_text = chatgpt_service.get_quick_health_advice(user_message)
                else:
                    response_text = chatgpt_service.get_chat_response(
                        user_message, 
                        conversation_history
                    )
            
            # Save bot response to database
            ChatHistory.objects.create(
                user=request.user,
                message=response_text,
                is_bot=True,
                message_type=chat_type
            )
            
            return JsonResponse({
                'response': response_text,
                'type': chat_type,
                'status': 'success'
            })
            
        except Exception as e:
            # Fallback to basic bot in case of errors
            bot = BasicHealthcareBot()
            response_text = bot.get_response("help")
            
            return JsonResponse({
                'response': response_text,
                'status': 'error',
                'message': 'Using fallback mode'
            })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def chat_history(request):
    """Get user's chat history"""
    chats = ChatHistory.objects.filter(user=request.user).order_by('created_at')[:50]
    chat_data = [
        {
            'message': chat.message,
            'is_bot': chat.is_bot,
            'timestamp': chat.created_at.isoformat(),
            'type': chat.message_type
        }
        for chat in chats
    ]
    return JsonResponse({'chats': chat_data})

# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from core.models import Patient, Doctor, Appointment, HealthRecord

def home(request):
    doctors = Doctor.objects.filter(available=True)[:6]
    return render(request, 'core/home.html', {'doctors': doctors})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create patient profile
            Patient.objects.create(user=user)
            
            # Auto login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')[:5]
        health_records = HealthRecord.objects.filter(patient=patient).order_by('-created_at')[:3]
        
        stats = {
            'total_appointments': appointments.count(),
            'upcoming_appointments': appointments.filter(status__in=['scheduled', 'confirmed']).count(),
            'health_records_count': health_records.count(),
        }
        
    except Patient.DoesNotExist:
        appointments = []
        health_records = []
        stats = {}
    
    return render(request, 'core/dashboard.html', {
        'appointments': appointments,
        'health_records': health_records,
        'stats': stats
    })