from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from law.models import Law, FavoriteLaw
from law.serializers import LawSerializer, FavoriteLawSerializer
from news_npo.permissions import IsClient


class LawGetPostAPIView(APIView, PageNumberPagination):
    allow_methods = ['GET', 'POST']
    serializer_class = LawSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        law = Law.objects.filter(Q(title__contains=query) |
                                 Q(description__contains=query))
        results = self.paginate_queryset(law,
                                         request,
                                         view=self)

        return self.get_paginated_response(self.serializer_class(results,
                                                                 many=True).data)

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        law = Law.objects.create(title=title,
                                 description=description)
        law.save()
        return Response(data=self.serializer_class(law).data,
                        status=status.HTTP_201_CREATED)


class LawDeletePutAPIViewDetail(APIView):
    allow_methods = ['GET', 'DELETE', 'PUT']
    serializer_class = LawSerializer

    def get(self, request, id):
        law = Law.objects.get(id=id)
        return Response(data=self.serializer_class(law).data)

    def delete(self, request, *args, **kwargs):
        law = Law.objects.get(id=id)
        law.delete()
        laws = Law.objects.all()
        return Response(data=self.serializer_class(laws).data,
                        status=status.HTTP_200_OK)

    def put(self, request, id):
        law = Law.objects.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        law.title = title
        law.description = description
        law.save()

        return Response(data=self.serializer_class(law).data,
                        status=status.HTTP_200_OK)


class FavoriteLawCreateListDestroyAPIView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        law_id = int(request.data.get('law_id'))
        try:
            favorite = FavoriteLaw.objects.get(law_id=law_id,
                                               user=request.user)
        except:
            favorite = FavoriteLaw.objects.create(law_id=law_id,
                                                  user=request.user)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoriteLawSerializer(favorite).data)

    def get(self, request):
        favorites = FavoriteLaw.objects.filter(user=request.user)
        return Response(data=FavoriteLawSerializer(favorites,
                                                   many=True).data,
                        status=status.HTTP_200_OK)

    def delete(self, request):
        law_id = int(request.data.get('law_id'))
        favorites = FavoriteLaw.objects.filter(law_id=law_id,
                                               user=request.user)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)
