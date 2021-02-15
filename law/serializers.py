from rest_framework import serializers
from law.models import Law, FavoriteLaw
from news_npo.serializers import UserSerializer


class LawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Law
        fields = '__all__'

class FavoriteLawSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    law = LawSerializer()

    class Meta:
        model = FavoriteLaw
        fields = 'id user law'.split()