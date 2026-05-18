# TeleMed — Virtual Healthcare & AI Triage Platform

TeleMed is a secure, responsive full-stack telemedicine web application designed to streamline virtual patient care, dynamic scheduling, and clinical routing. The platform features an integrated, automated AI medical assistant powered by the Google Gemini SDK to help users navigate platform features, answer general health FAQs, and provide concise self-care guidance with appropriate medical disclaimers.

## 🚀 Key Features

* **Dynamic Patient Registration:** Secure account creation and authentication powered by Django's robust user management.
* **Vitals & Health Tracking:** Integrated biometric logging module allowing patients to input critical records (heart rate, weight, etc.) for physician evaluation.
* **Gemini AI Chatbot Wrapper:** A customized `gemini-1.5-flash` engine pre-configured with strict system instructions to guide patient triage, platform navigation, and symptom checking safely.
* **Responsive Architecture:** Fully styled with a clean Bootstrap 5 layout and crisp form styling via `django-crispy-forms`.

## 🛠️ Tech Stack

* **Backend Framework:** Python / Django 6.x
* **AI Integration:** Google Generative AI SDK (Gemini)
* **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
* **Forms Rendering:** Django Crispy Forms (Bootstrap 5 Template Pack)
* **Database:** SQLite (Development standard)

## 💻 Local Installation & Setup

Follow these steps to get a local development copy up and running:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/Healthcare-Telemedicine.git](https://github.com/YOUR_GITHUB_USERNAME/Healthcare-Telemedicine.git)
cd Healthcare-Telemedicine
