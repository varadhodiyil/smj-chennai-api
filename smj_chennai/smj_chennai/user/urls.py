from django.urls import path
from smj_chennai.user import views

urlpatterns = [path("", views.ProfileApiView.as_view())]
