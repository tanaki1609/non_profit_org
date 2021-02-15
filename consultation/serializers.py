from rest_framework import serializers

from consultation.models import Question, AdminAnswer


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = 'id text answers'.split()

        comments = serializers.SerializerMethodField()

    def get_answers(self, obj):
        answers = AdminAnswer.objects.filter(question=obj)
        return AdminAnswerSerializer(answers, many=True).data


class AdminAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAnswer
        fields = 'id text'.split()