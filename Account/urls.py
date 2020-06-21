from django.urls import path
from Account import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('register', views.registration_view, name="registration"),
    path('login', views.login_view, name="login"),
    path('update', views.update_user_detail_view, name="updat_user_detail"),
    path('request_password_update',views.request_password_update, name="request_password_update"), 
    path('confirm_user_passcode', views.confirm_user_passcode, name="confirm_user_passcode"),
    path('reset_password', views.reset_password, name="reset_password"),
    path('users', views.user_list_view),
    path('<str:username>', views.user_detail_view, name="user_detail"),
    path('<str:username>/user_reactions', views.user_detail_view_reactions, name="user detail and reactions"),

]
