from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.chatgpt_api, name='chatgpt_api'),
    path('history/', views.chat_history, name='chat_history'),
]