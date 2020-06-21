from Account.models import UserAccount
from django.db import models
from BlogPost.models import BlogArticle
from datetime import datetime

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="author")
    time = models.DateTimeField()
    content = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
