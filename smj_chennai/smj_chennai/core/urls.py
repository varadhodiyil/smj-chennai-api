from django.urls import path
from smj_chennai.core import views

urlpatterns = [
    path("documents/", views.DocumentsAPI.as_view()),
    path("documents/<int:docket_number>/", views.DocumentUpdateAPI.as_view()),
    path("charges/", views.ChargesAPI.as_view()),
    path("charges/<int:id>/", views.ChargesUpdateAPI.as_view()),
    path("party/", views.PartyAPI.as_view()),
]
