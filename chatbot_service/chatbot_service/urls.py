from django.urls import path
from .views import ChatbotQuery

urlpatterns = [
    path('query/', ChatbotQuery.as_view(), name='chatbot-query'),
]