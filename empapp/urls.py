from django.urls import path

from empapp import views

urlpatterns = [

    path("emp/", views.EmployeeAPIView.as_view()),
    path("emp/<str:pk>/", views.EmployeeAPIView.as_view()),
]
