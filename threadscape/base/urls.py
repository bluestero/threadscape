from django.urls import path
from . import views


#-URL patterns for the base app path-#
urlpatterns = [
    path("", views.home, name = "home"),
    path("login/", views.login_page, name = "login-page"),
    path("logout/", views.logout_user, name = "logout-user"),
    path("thread/<str:pk>/", views.thread, name = "thread"),
    path("create-thread/", views.create_thread, name = "create-thread"),
    path("update-thread/<str:pk>/", views.update_thread, name = "update-thread"),
    path("delete-thread/<str:pk>/", views.delete_thread, name = "delete-thread"),
]
