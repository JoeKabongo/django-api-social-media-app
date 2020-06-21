from rest_framework import serializers
from datetime import datetime

from .models import Comment, Reply, Reaction



class CommentSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('time_format')
    username = serializers.SerializerMethodField('display_username')
    profileImage = serializers.SerializerMethodField('get_profile')
    replies = serializers.SerializerMethodField('count_replies')
    isLiked = serializers.SerializerMethodField('is_liked')
    isDisliked = serializers.SerializerMethodField('is_disliked')
    likes = serializers.SerializerMethodField('count_likes')
    dislikes = serializers.SerializerMethodField('count_dislikes')


    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'profileImage', 'article', 'time', 'content',  'likes', 'dislikes', 'username', 'replies', 'isLiked', 'isDisliked']

    def display_username(self, comment):
        return comment.user.get_username()
    
    def get_profile(self, comment):
        return comment.user.get_profileImage()
        

    def create(self, validated_data):
        """ Creates and returns a new user """
        new_post = Comment(
            user=validated_data.get('user'),
            article=validated_data.get('article'),
            post=validated_data.get('post'),
            content= validated_data.get('content'),
            time = datetime.utcnow()
        )

       
        new_post.save()
        return new_post

    def update(self, comment, validated_data):
        comment.content = validated_data.get('content')
        comment.save()
        return comment
        
    def time_format(self, comment):
        new_time = comment.time.strftime("%m/%d/%Y %I:%M:%S %p UTC")
        return new_time

    def count_replies(self, comment):
        replies = Reply.objects.filter(parentComment=comment.id)
        return len(replies)

    def count_likes(self, comment):
        reactions = Reaction.objects.filter(reply__isnull=True).filter(comment=comment.id).filter(like=True)
        return len(reactions)
    
    def count_dislikes(self, comment):
        reactions = Reaction.objects.filter(reply__isnull=True).filter(comment=comment.id).filter(dislike=True)
        return len(reactions)
    
    def is_liked(self, comment):
        return False
     
    
    def is_disliked(self, comment):
        return False
    


class ReplySerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('time_format')
    username = serializers.SerializerMethodField('display_username')
    profileImage = serializers.SerializerMethodField('get_profile')
    likes = serializers.SerializerMethodField('count_likes')
    dislikes = serializers.SerializerMethodField('count_dislikes')
    isLiked = serializers.SerializerMethodField('is_liked')
    isDisliked = serializers.SerializerMethodField('is_disliked')

    class Meta:
        model = Reply
        fields = ['id', 'user', 'post', 'article', 'parentComment', 'profileImage',  'time', 'content', 'username', 'likes', 'dislikes', 'isLiked', 'isDisliked']

    def display_username(self, comment):
        return comment.user.get_username()
    
    def get_profile(self, comment):
        return comment.user.get_profileImage()
        
    def create(self, validated_data):
        """ Creates and returns a new user """
        new_reply = Reply(
            user=validated_data.get('user'),
            parentComment=validated_data.get('parentComment'),
            article=validated_data.get('article'),
            post=validated_data.get('post'),
            content= validated_data.get('content'),
            time = datetime.utcnow()
        )

       
        new_reply.save()
        return new_reply
    
    def update(self, reply, validated_data):
        reply.content = validated_data.get('content')
        reply.save()
        print('SAVE IT BRO')
        return reply

    def time_format(self, post):
        new_time = post.time.strftime("%m/%d/%Y %I:%M:%S %p UTC")
        return new_time

    def count_likes(self, reply):
        reactions = Reaction.objects.filter(reply=reply.id).filter(like=True)
        return len(reactions)
    
    def count_dislikes(self, reply):
        reactions = Reaction.objects.filter(reply=reply.id).filter(dislike=True)
        return len(reactions)

    
    def is_liked(self, reply):
        return False
    
    def is_disliked(self, reply):
        return False


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['id', 'user', 'post', 'comment', 'reply', 'like', 'dislike']
    