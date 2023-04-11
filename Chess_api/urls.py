"""
URL configuration for Chess_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from My_plat.views import AuthViewSet
from Chess import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('GPT_turbo', views.GPT_turbo),    
    path("GPT", views.GPT),    
    path('transcription1', views.transcribe_v1),  
    path('transcription2', views.transcribe_v2),  
    path("Texttoaudio", views.text_to_audio_vieww),
    path("audiotoaudio", views.audio_to_audio),   
    path("get/quiz", views.send_question),   
    path("get/response", views.check_answer),   
    
]

