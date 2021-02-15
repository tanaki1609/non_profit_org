from django.db import models
from news_npo.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()


    def __str__(self):
        return self.text

    def view_answers(self):
        return AdminAnswer.objects.filter(text=self)

class AdminAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='answers')
    text = models.TextField()


    def __str__(self):
        return self.text