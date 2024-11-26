from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name = "home"),
    path("thread/<str:pk>/", views.thread, name = "thread"),
    path("create-thread/", views.create_thread, name = "create-thread")
]
