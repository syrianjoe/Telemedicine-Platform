from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Simple home page view
def home(request):
    return HttpResponse("""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
            <h1 style="color: #2563eb;">🏥 Healthcare Telemedicine Platform</h1>
            <p style="font-size: 18px; color: #4b5563;">
                Congratulations! Your Django server is running! 🚀
            </p>
            <p>If you can see this message, everything is working correctly.</p>
            <div style="margin-top: 30px;">
                <a href="/admin" style="background: #2563eb; color: white; padding: 10px 20px; 
                   text-decoration: none; border-radius: 5px; margin: 10px;">
                    Go to Admin
                </a>
            </div>
        </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)