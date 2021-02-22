from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from consultation.models import Question
from consultation.serializers import QuestionSerializer


class QuestionAPIView(ListCreateAPIView):
    allow_methods = ['GET', 'POST']
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        question = Question.objects.all()
        return Response(data=self.serializer_class(question, many=True).data)

    def create(self, request, *args, **kwargs):
        text = request.data.get('text')
        question = Question.objects.create(text=text)
        question.save()
        return Response(data=self.serializer_class(question).data,
                        status=status.HTTP_201_CREATED)
