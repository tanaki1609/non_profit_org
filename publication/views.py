from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from news_npo.permissions import IsClient
from publication.models import Publication, FavoritePublication
from publication.serializers import PublicationSerializer, FavoritePublicationSerializer


class PublicationListCreateAPIView(APIView, PageNumberPagination):
    allow_methods = ['GET', 'POST']
    serializer_class = PublicationSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        publication = Publication.objects.filter(Q(title__contains=query) |
                                                 Q(description__contains=query))
        results = self.paginate_queryset(publication,
                                         request,
                                         view=self)

        return self.get_paginated_response(self.serializer_class(results,
                                                                 many=True).data)

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        publication = Publication.objects.create(title=title,
                                                 description=description)
        publication.save()
        return Response(data=self.serializer_class(publication).data,
                        status=status.HTTP_201_CREATED)


class PublicationDeletePutGetAPIViewDetail(APIView):
    allow_methods = ['GET', 'DELETE', 'PUT']
    serializer_class = PublicationSerializer

    def get(self, request, id):
        publication = Publication.objects.get(id=id)
        return Response(data=self.serializer_class(publication).data)

    def delete(self, request, *args, **kwargs):
        publication = Publication.objects.get(id=id)
        publication.delete()
        publication = Publication.objects.all()
        return Response(data=self.serializer_class(publication).data,
                        status=status.HTTP_200_OK)

    def put(self, request, id):
        publication = Publication.objects.get(id=id)
        title = request.data.get('title')
        description = request.data.get('description')
        publication.title = title
        publication.description = description
        publication.save()

        return Response(data=self.serializer_class(publication).data,
                        status=status.HTTP_200_OK)


class FavoritesPubsCreateListDestroyAPIView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        publication_id = int(request.data.get('publication_id'))
        try:
            favorite = FavoritePublication.objects.get(publication_id=publication_id,
                                                       user=request.user)
        except:
            favorite = FavoritePublication.objects.create(publication_id=publication_id,
                                                          user=request.user)
            favorite.save()
        return Response(status=status.HTTP_200_OK,
                        data=FavoritePublicationSerializer(favorite).data)

    def get(self, request):
        favorites = FavoritePublication.objects.filter(user=request.user)
        return Response(data=FavoritePublicationSerializer(favorites,
                                                           many=True).data,
                        status=status.HTTP_200_OK)

    def delete(self, request):
        publication_id = int(request.data.get('publication_id'))
        favorites = FavoritePublication.objects.filter(publication_id=publication_id,
                                                       user=request.user)
        favorites.delete()
        return Response(status=status.HTTP_200_OK)
