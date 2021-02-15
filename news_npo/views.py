from datetime import datetime, timedelta
from random import randint
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from news_npo.models import News, User, ConfirmationCode, FavoriteNews
from news_npo.permissions import IsClient
from news_npo.serializers import NewsSerializer, FavoriteNewsSerializer


class NewsAPIView(APIView, PageNumberPagination):
    allow_methods = ['GET', 'POST']
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        news = News.objects.filter(Q(title__contains=query) |
                                   Q(description__contains=query))
        results = self.paginate_queryset(news,
                                         request,
                                         view=self)

        return self.get_paginated_response(self.serializer_class(results,
                                                                 many=True,
                                           context={'request': request}).data)

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        news = News.objects.create(title=title,
                                   description=description)
        news.save()
        return Response(data=self.serializer_class(news).data,
                        status=status.HTTP_201_CREATED)


class NewsAPIViewDetail(APIView):
    allow_methods = ['GET', 'DELETE', 'PUT']
    serializer_class = NewsSerializer

    def get(self, request, id):
        news = News.objects.get(id=id)
        return Response(data=self.serializer_class(news).data)

    def delete(self, request, *args, **kwargs):
        news = News.objects.get(id=id)
        news.delete()
        news = News.objects.all()
        return Response(data=self.serializer_class(news).data,
                        status=status.HTTP_200_OK)

    def put(self, request, id):
        news = News.objects.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        news.title = title
        news.description = description
        news.save()

        return Response(data=self.serializer_class(news).data,
                        status=status.HTTP_200_OK)


class RegisterApiView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create(username=username,
                                   password=password,
                                   is_active=False)
        user.save()
        code = randint(1111, 9999)
        confirmation_code = ConfirmationCode()
        confirmation_code.code = str(code)
        confirmation_code.user = user
        confirmation_code.valid_until = datetime.now() + timedelta(minutes=20)
        confirmation_code.save()
        return Response(status=status.HTTP_200_OK)


class ConfirmApiView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')

        codes = ConfirmationCode.objects.get(code=code,
                                             valid_until__gte=datetime.now())
        user = codes.user
        user.is_active = True
        user.save()
        codes.delete()
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={'token': token.key},
                        status=status.HTTP_200_OK)


class LoginApiView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'],
                            password=request.data.get('password', 'admin123'))
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User not found'})
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class FavoriteCreateListDestroyAPIView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        news_id = int(request.data.get('news_id'))
        try:
            favorite = FavoriteNews.objects.get(news_id=news_id,
                                                user=request.user)
        except:
            favorite = FavoriteNews.objects.create(news_id=news_id,
                                                   user=request.user)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoriteNewsSerializer(favorite).data)

    def get(self, request):
        favorites = FavoriteNews.objects.filter(user=request.user)
        return Response(data=FavoriteNewsSerializer(favorites,
                                                    many=True).data,
                        status=status.HTTP_200_OK)

    def delete(self, request):
        news_id = int(request.data.get('news_id'))
        favorites = FavoriteNews.objects.filter(news_id=news_id,
                                                user=request.user)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)
