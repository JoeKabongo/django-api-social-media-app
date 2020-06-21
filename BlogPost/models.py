from django.db import models
from ckeditor.fields import RichTextField 
from Account.models import UserAccount
from datetime import datetime

# Create your models here.
class BlogArticle(models.Model):
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="article_author")
    title = models.CharField(max_length=50)
    coverImage = models.CharField(max_length=1000, default="None")
    body = RichTextField(null=True)
    blurb = models.CharField(max_length=200, default="")
    lastEdited = models.DateTimeField()
    datePublished = models.DateTimeField(null=True) #when it was published
    isPublished = models.BooleanField(default=False)

    def publish(self):
        self.isPublished = True
        self.datePublished = datetime.utcnow()
        self.save()
    
    def unpublish(self):
        self.isPublished = False
        self.datePublished = None
        self.save()
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    name=models.CharField(max_length=50)
    blogArticles = models.ManyToManyField(BlogArticle, related_name="blog_post")