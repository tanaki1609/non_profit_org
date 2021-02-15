from django.urls import path
from . import views as law

urlpatterns = [
    path('api/v1/laws/', law.LawGetPostAPIView.as_view()),
    path('api/v1/laws/<int:id>/', law.LawDeletePutAPIViewDetail.as_view()),
    path('api/v1/favouriteslaw/', law.FavoriteLawCreateListDestroyAPIView.as_view()),

]