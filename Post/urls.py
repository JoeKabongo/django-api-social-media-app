from django.urls import path, re_path
from Post import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    # path('reactions', views.get_reactions, name="view reactions"),
    path('save', views.create_post, name="save_post"), #save post
    path('edit_post', views.edit_post, name="edit post"),
    path('posts', views.post_list, name="all_post"),  #list of all post
    path('posts_user_reactions', views.post_list_user_reactions, name="all post and user reactions"),
    path('delete_post/<int:postId>', views.delete_post, name="delete_post"),


    path('<int:postId>', views.post_detail, name="post_detail"), #get a particular post and the username reaction to post
    path('<int:postId>/<username>', views.post_detail_user_reaction, name="post_detail"), #get a particular post and the username reaction to post
    path('like_post/<postId>', views.like_post, name="like post"),
    path('dislike_post/<postId>', views.dislike_post, name="dislike post"),
    path('remove_reaction/<reactionId>', views.remove_reaction, name="remove reaction ")


]
