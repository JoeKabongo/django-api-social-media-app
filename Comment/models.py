from django.db import models
from Post.models import Post
from Account.models import UserAccount
from BlogPost.models import BlogArticle

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="post")
    article = models.ForeignKey(BlogArticle, null=True, on_delete=models.CASCADE, related_name="blog_article")
    time = models.DateTimeField()
    content = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)


class Reply(models.Model):
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL, related_name="user_reply")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="parent_post")
    article = models.ForeignKey(BlogArticle, null=True, on_delete=models.CASCADE, related_name="parent_article")
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="parent_comment")
    time = models.DateTimeField()
    content = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class Reaction(models.Model):
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL, related_name="user_like")
    article = models.ForeignKey(BlogArticle, null=True, on_delete=models.CASCADE, related_name="article")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="related_post")
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE, related_name="related_comment")
    reply = models.ForeignKey(Reply, null=True, on_delete=models.CASCADE, related_name="related_reply")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


