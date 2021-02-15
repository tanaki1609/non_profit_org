from django.urls import path
from . import views as publication

urlpatterns = [
    path('api/v1/publication/', publication.PublicationListCreateAPIView.as_view()),
    path('api/v1/publication/<int:id>/', publication.PublicationDeletePutGetAPIViewDetail.as_view()),
    path('api/v1/favouritespub/', publication.FavoritesPubsCreateListDestroyAPIView.as_view()),

]