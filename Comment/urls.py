from django.urls import path, re_path
from Comment import views

urlpatterns = [
    path('post_comments/<postId>', views.get_post_comments, name="post_comment"),
    path('post_comments/<postId>/user_reactions', views.post_comments_user_reactions, name="comments and user reactions"),
    path('article_comments/<articleId>', views.get_article_comments, name="article comment"),
    path('article_comments/<articleId>/user_reactions', views.article_comments_user_reactions, name="post_comment"),


    path('save_comment', views.save_comment, name="save_comment"),
    path('edit_comment/<commentId>', views.edit_comment, name="edit comment"),
    path('delete_comment/<commentId>', views.delete_comment, name="delete a comment"),
    path('like_comment/<articleId>/<postId>/<commentId>', views.like_comment, name="like comment"),
    path('dislike_comment/<articleId>/<postId>/<commentId>', views.dislike_comment, name="dislike comment"),
    path('delete_reaction/<reactionId>', views.delete_reaction, name="delete reaction"),



    path('replies/<commentId>', views.get_replies_to_comment, name="get replies to comment"),
    path('replies/<commentId>/user_reactions', views.replies_to_comment_user_reactions, name="replies to comment and user reaction"),
    path('save_reply/<articleId>/<postId>/<commentId>', views.save_reply, name="save reply"),
    path('edit_reply/<replyId>', views.edit_reply, name="edit reply"),
    path('delete_reply/<replyId>', views.delete_reply, name="delete reply"),
    path('like_reply/<commentId>/<replyId>', views.like_reply, name="reply reply"),
    path('dislike_reply/<commentId>/<replyId>', views.dislike_reply, name="reply")



]


