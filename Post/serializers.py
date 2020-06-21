from .models import Post
from Account.models import UserAccount
from Comment.models import Comment, Reaction, Reply
from rest_framework import serializers
from datetime import datetime


class PostSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('time_format')
    username = serializers.SerializerMethodField('display_username')
    profileImage = serializers.SerializerMethodField('profile_image')
    comments = serializers.SerializerMethodField('count_comments')
    likes = serializers.SerializerMethodField('count_likes')
    dislikes = serializers.SerializerMethodField('count_dislikes')
    isLiked = serializers.SerializerMethodField('is_liked')
    isDisliked = serializers.SerializerMethodField('is_disliked')

    class Meta:
        model = Post
        fields = ['id', 'user','content', 'profileImage', 'time', 'likes', 'dislikes', 'comments', 'username', 'isLiked', 'isDisliked']
    
    def display_username(self, post):
        return post.user.get_username()
    
    def profile_image(self, post):
        return post.user.get_profileImage()
        

    def create(self, validated_data):
        """ Creates and returns a new user """
        new_post = Post(
            user=validated_data.get('user'),
            content= validated_data.get('content'),
            time = datetime.utcnow()
        )

        new_post.save()
        return new_post
    
    def update(self, post, validated_data):
        post.content = validated_data.get('content')
        post.save()
        return post

    def time_format(self, post):
        new_time = post.time.strftime("%m/%d/%Y %I:%M:%S %p UTC")
        return new_time

    def count_comments(self, post):
        comments = Comment.objects.filter(post=post.id)
        replies = Reply.objects.filter(post=post.id)
        return len(comments) + len(replies)

    def count_likes(self, post):
        likes = Reaction.objects.filter(post=post.id).filter(reply=None).filter(comment=None).filter(like=True)
        return len(likes)
    
    def count_dislikes(self, post):
        dislikes = Reaction.objects.filter(post=post.id).filter(reply=None).filter(comment=None).filter(dislike=True)
        return len(dislikes)
        
    def is_liked(self, post):
        return False
    
    def is_disliked(self, post):
        return False
    

