import google.generativeai as genai
from django.conf import settings

class HealthcareChatGPT:
    def __init__(self):
        # Configure the Gemini SDK with your API key
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # System instructions to guide Gemini's persona and rules
        self.system_instruction = """
        You are a helpful healthcare assistant for a telemedicine platform called "TeleMed".
        1. Navigation: Guide users to appointments, health records, or dashboard.
        2. Healthcare Guidance: General tips and symptom checking with disclaimers.
        3. Appointment Management: Booking procedures and cancellation policies.

        DISCLAIMERS: ALWAYS state: "I am an AI assistant, not a medical doctor." For emergencies, call emergency services immediately.
        """
        
        # Initialize the model with system instructions pre-configured
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.system_instruction
        )

    def get_chat_response(self, user_message, conversation_history=None):
        try:
            chat = self.model.start_chat(history=[])
            response = chat.send_message(user_message)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I apologize, but I am unable to respond at the moment."

    def get_quick_health_advice(self, symptom):
        try:
            prompt = f"A user is asking about: {symptom}. Provide self-care tips and clarify when they should see a doctor. Keep it concise."
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "Please consult a healthcare professional for medical concerns."


# ADDING THIS CLASS TO PREVENT THE IMPORT ERROR IN VIEWS.PY
class BasicHealthcareBot:
    """A fallback chatbot helper required by views.py routing configuration."""
    def __init__(self):
        # Dynamically reference the primary Gemini configuration
        self.engine = HealthcareChatGPT()

    def get_response(self, message):
        try:
            return self.engine.get_chat_response(message)
        except Exception:
            return "System navigation is currently unavailable."