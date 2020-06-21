from django.urls import path, re_path
from home import views

urlpatterns = [
    path('', views.goHome, name="post_comment"),
]


