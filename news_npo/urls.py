from django.urls import path
from . import views as news_npo

urlpatterns = [
    path('api/v1/news/', news_npo.NewsAPIView.as_view()),
    path('api/v1/news/<int:id>/', news_npo.NewsAPIViewDetail.as_view()),
    path('api/v1/register/', news_npo.RegisterApiView.as_view()),
    path('api/v1/confirm/', news_npo.ConfirmApiView.as_view()),
    path('api/v1/login/', news_npo.LoginApiView.as_view()),
    path('api/v1/favourites/', news_npo.FavoriteCreateListDestroyAPIView.as_view()),

]