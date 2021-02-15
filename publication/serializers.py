from rest_framework import serializers
from news_npo.serializers import UserSerializer
from publication.models import Publication, FavoritePublication


class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = '__all__'

class FavoritePublicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    publication = PublicationSerializer()

    class Meta:
        model = FavoritePublication
        fields = 'id user publication'.split()