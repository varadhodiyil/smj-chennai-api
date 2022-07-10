from django.urls import path
from smj_chennai.core import views

urlpatterns = [
    path("documents/", views.DocumentsAPI.as_view()),
    path("charges/", views.ChargesAPI.as_view()),
]
