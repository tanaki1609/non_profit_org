from django.urls import path
from . import views as consultation

urlpatterns = [
    path('api/v1/consult/', consultation.QuestionAPIView.as_view()),

]