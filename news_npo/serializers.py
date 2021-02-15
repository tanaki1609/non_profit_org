
from rest_framework import serializers
from .models import User, FavoriteNews, NewsImage
from news_npo.models import News


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = 'id title description image created_date link images is_favourite'.split()

    def get_is_favourite(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        else:
            favorite = FavoriteNews.objects.filter(news=obj, user=request.user)
            if len(favorite) > 0:
                return True
            else:
                return False


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'id username'.split()

class FavoriteNewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    news = NewsSerializer()

    class Meta:
        model = FavoriteNews
        fields = 'id user news'.split()