from rest_framework import serializers
from datetime import datetime

from Comment.models import Comment, Reply
from .models import BlogArticle



class BlogRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogArticle
        fields = ['id' , 'author', 'title', 'datePublished', 'body', 'blurb', 'isPublished', 'coverImage']
    
    def create(self, validated_data):
        """ Creates and returns a new blog post """
        print(validated_data)
        new_blog = BlogArticle(
            author=validated_data.get('author'),
            title= validated_data.get('title'),
            lastEdited = datetime.utcnow(),
            isPublished = validated_data.get('isPublished'),
            body = validated_data.get('body'),
            blurb = validated_data.get('blurb'),
            coverImage = validated_data.get('coverImage')
        )
        if validated_data.get('isPublished'):
            new_blog.datePublished = datetime.utcnow()
        
        new_blog.save()
        return new_blog
    
    def update(self, article, validated_data):
        """
            update article 
        """
        article.title = validated_data.get('title')
        article.lastEdited = datetime.utcnow()
        
        #update published date if the isPublished value has changed
        if not article.isPublished and validated_data.get('isPublished'):
            article.datePublished = datetime.utcnow()
        
        if article.isPublished and not validated_data.get('isPublished'):
            article.datePublished = None
        

        article.coverImage = validated_data.get('coverImage')
    
        article.isPublished = validated_data.get('isPublished')
        
        article.body = validated_data.get('body')
        article.blurb = validated_data.get('blurb')
        article.save()
        return article
    

    

class BlogSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField('format_author')
    datePublished = serializers.SerializerMethodField('published_format')
    comments = serializers.SerializerMethodField('count_comments')


    class Meta:
        model = BlogArticle
        fields = ['id' , 'author', 'authorName', 'title', 'datePublished', 'body', 'blurb', 'isPublished', 'lastEdited', 'coverImage', 'comments']
    
    def format_author(self, blog):
        return blog.author.get_username()

    def published_format(self, blog):
        if blog.datePublished != None:
            new_time = blog.datePublished.strftime("%m/%d/%Y %I:%M:%S %p UTC")
            return new_time
        return None
    
    def count_comments(self, article):
        comments = Comment.objects.filter(article=article)
        replies = Reply.objects.filter(article=article)
        return len(comments) + len(replies)

    