from django.urls import path

from kitchen.views import index

urlpatterns = [
    path("", index, name="index"),
    path("dish", index),
]

app_name = "kitchen"
