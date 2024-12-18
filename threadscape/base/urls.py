from django.urls import path
from . import views


#-URL patterns for the base app path-#
urlpatterns = [
    path("", views.home, name = "home"),
    path("login/", views.login_page, name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("topics/", views.topics_page, name = "topics"),
    path("activity/", views.activity_page, name = "activity"),
    path("thread/<str:pk>/", views.thread, name = "thread"),
    path("register/", views.register_page, name = "register"),
    path("profile/<str:pk>/", views.profile, name = "profile"),
    path("create-thread/", views.create_thread, name = "create-thread"),
    path("update-profile/", views.update_profile, name = "update-profile"),
    path("update-thread/<str:pk>/", views.update_thread, name = "update-thread"),
    path("delete-thread/<str:pk>/", views.delete_thread, name = "delete-thread"),
    path("delete-message/<str:pk>/", views.delete_message, name = "delete-message"),
]
