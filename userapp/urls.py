from django.urls import path

from userapp import views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<str:id>/", views.UserView.as_view()),

    path("api_user/", views.UserAPIView.as_view()),
    path("api_user/<str:id>/", views.UserAPIView.as_view()),
]
