from django.urls import path, re_path
from BlogPost import views

urlpatterns = [    
    path('create', views.create_blog, name="create"),
    path('save', views.save_blog, name="edit"),
    path('publish/<articleId>', views.publish_blog, name="publish"),
    path('unpublish/<articleId>', views.unpublish_blog, name="publish"),


    path('delete/<id>', views.delete_blog, name="delete"),

    path('dashboard/<username>', views.author_dashboard, name=""),
    path('all', views.view_all, name="all"),
    path('recents/<count>', views.get_recents, name="get last count blog"),

    path('save_comment', views.save_comment, name="save comment"),
    path('edit_comment', views.edit_comment, name="edit comment"),
    path('delete_comment/<commentId>', views.delete_comment, name="delete comment"),

    path('save_like', views.save_like, name="save_like"),
    path('save_dislike', views.save_dislike, name="save_dislike"),
    path('delete_reaction/<reactionId>', views.delete_reaction, name="delete_reaction"),

    



    path('<articleId>', views.view_blog, name="view a blog"),

    path('<articleId>/<username>', views.view_blog_userReactions, name="blog and user reactions"),



]


