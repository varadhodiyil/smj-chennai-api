from django.urls import path
from smj_chennai.dashboard import views

urlpatterns = [
    path("party", views.PartyBalanceApi.as_view()),
    path("summary", views.SummaryApi.as_view()),
]
