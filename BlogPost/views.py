from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
import json
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


import cloudinary
import cloudinary.uploader
import cloudinary.api

from Account.models import UserAccount
from Post.models import Post
from .models import BlogArticle
from .serializers import BlogSerializer, BlogRegistrationSerializer
import json
from config.cloudinary import cloud_name, api_key, api_secret

cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = api_key, 
  api_secret = api_secret 
)

@api_view(['POST',])
@parser_classes([JSONParser, FormParser, MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_blog(request):
    """
        Create a new blog article
    """
    #gather all the data required for blog article
    try:
        coverImage = cloudinary.uploader.upload(request.data['coverImage']).get('url')
        data = {
            'title' : request.data['title'],
            'author' : request.user.id,
            'body' : request.data['body'],
            'blurb' : request.data['blurb'],
            'coverImage' : coverImage,
            'isPublished': True
        }
        if request.data['isPublished'].lower() != 'true':
            data['isPublished'] = False 

    except KeyError:
        return Response(data={'message': 'Something was wrong in your request'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BlogRegistrationSerializer(data=data)

    #make sure the data provided is valid
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data,  status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
  
        
@api_view(['PUT',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_blog(request):
    """
        save/update a  blogpost
    """
    try:
        
        data = {
            'id' : request.data['id'],
            'title': request.data['title'],
            'body': request.data['body'],
            'author': request.user.id,
            'blurb': request.data['blurb'],
            'isPublished' : True

        }

        if request.data['isPublished'].lower() != 'true':
            data['isPublished'] = False 
        
        if request.data.get('coverImage') != None:
            coverImage = cloudinary.uploader.upload(request.data['coverImage']).get('url')
            data['coverImage'] = coverImage
        else:
            data['coverImage'] = None
        


    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    #find the article in the database, ensuring it exist
    try:
        blog = BlogArticle.objects.get(pk=data.get('id'))
    except BlogArticle.DoesNotExist:
        return Response(data={'message': 'Blog article not found'}, status=status.HTTP_404_NOT_FOUND)

    if data['coverImage'] == None:
        data['coverImage'] = blog.coverImage
        
    serializer = BlogRegistrationSerializer(blog, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    print(serializer.errors)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def publish_blog(request, articleId):
    """
        Publish an article
    """
    try:
        blog = BlogArticle.objects.get(pk=articleId)
    except BlogArticle.DoesNotExist:
        return Response(data={'message': 'Blog article was not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        blog.publish() 
    except:
        return Response(data={'message': 'Something went wrong, try again'}, status=status.HTTP_304_NOT_MODIFIED) 
     
    return Response(data={'message': 'blog was published'}, status=status.HTTP_200_OK)


@api_view(['PUT',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unpublish_blog(request, articleId):
    """
        Publish an article
    """
    try:
        blog = BlogArticle.objects.get(pk=articleId)
    except BlogArticle.DoesNotExist:
        return Response(data={'message': 'Blog article was not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        blog.unpublish() 
    except:
        return Response(data={'message': 'Something went wrong, try again'}, status=status.HTTP_304_NOT_MODIFIED) 
     
    return Response(data={'message': 'blog was unpublished'}, status=status.HTTP_200_OK)




@api_view(['DELETE',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_blog(request, id):
    """
        deleting a blog
    """

    #make sure the blog post exist first
    try:
        blog = BlogArticle.objects.get(pk=id)
    except BlogArticle.DoesNotExist:
        return Response(data={"message" : "blogpost was not found"}, status=status.HTTP_404_NOT_FOUND)


    
    #double check that the author of the blog is the user that is trying to delete it
    if blog.author != request.user:
        return Response(data={"message" : "You are not allowed to delete this post"}, status=status.HTTP_401_UNAUTHORIZED)

    blog.delete()
    return Response(data={"message": "article have been removed" }, status=status.HTTP_200_OK)



@api_view(['GET'])
def view_all(request):
    """
        View all posts
    """
    blogs = BlogArticle.objects.filter(isPublished=True)
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_recents(request, count):
    """
        Get recents count articles
    """
    try:
        count = int(count)
    except:
        count = 3 
    blogs = BlogArticle.objects.filter(isPublished=True).order_by('-datePublished')[:count]
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET',])
def view_blog(request, articleId):
    """
        View a post with id
    """

    #make sure the article exist in the database and get its data
    try:
        blog = BlogArticle.objects.get(pk=articleId)
    except BlogArticle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    blog_serializer = BlogSerializer(blog)

    # #grap the comment associated with this article
    # comments = Comment.objects.filter(blogArticle=articleId)
    # comment_serializer = CommentSerializer(comments, many=True)


    

    # #put both serializer in an array
    # all_serializers = [blog_serializer.data, comment_serializer.data, []]

    # response = {
    #     'data': all_serializers
    # }
    return Response(data=blog_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def view_blog_userReactions(request, articleId, username):
    #make sure the article exist in the database and get its data

    print('inside here')
    try:
        blog = BlogArticle.objects.get(pk=articleId)
    except BlogArticle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    blog_serializer = BlogSerializer(blog)

    #grap the comment associated with this article
    # comments = Comment.objects.filter(blogArticle=articleId)
    # comment_serializer = CommentSerializer(comments, many=True)


    # try:
    #     user = UserAccount.objects.get(username=username)
    #     reactions = Reaction.objects.filter(article=articleId).filter(user=user.id).filter(reply__isnull=True)
    #     reactions_serializer = ReactionSerializer(reactions, many=True)
    #     all_reactions = reactions_serializer.data

    # except UserAccount.DoesNotExist:
    #     all_reactions = []

   
    #put both serializer in an array
    # all_serializers = [blog_serializer.data, comment_serializer.data, all_reactions]

    # response = {
    #     'data': all_serializers
    # }
    return Response(data=blog_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def author_dashboard(request, username):
    """
        Get articles written by this author
    """
    try:
        user = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        return Response(data= {'message': 'this user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    blogs = BlogArticle.objects.filter(author=user)
    serializer = BlogSerializer(blogs, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_comment(request):
    """
        Add a comment to an article
    """

    try:
        data ={
            'blogArticle': request.data['blogArticleId'],
            'user' : request.user.id,  
            'content' : request.data['content']
        }
    except:
        return Response(data={'message': 'Something was wrong in your request'}, status=status.HTTP_400_BAD_REQUEST)
    
    comment_serializer = CommentSerializer(data=data)

    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(data=comment_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_comment(request):
    """
        edit a comment
    """
    try:
        user = request.user
        data = {
            'content': request.data['content'],
            'commentId': request.data['commentId'],
            'user':  user.id,
        }
    
    except :
       return Response(data={'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
   

    #make sure the comment exisit
    try:
        comment = Comment.objects.get(pk=data['commentId'])

         #extra check to make sure this comment is associated with our user
        if comment.user != request.user:
            return Response(
                data={'message': 'You are not authorized to edit this post'}, 
                status=status.HTTP_401_UNAUTHORIZED )

        serializer = CommentSerializer(comment, data=data)

    except Comment.DoesNotExist:
       return Response(data={'message': 'Comment was not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    #make sur the serializer is valid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #for some reasons the serializer was not valid
    else:
        return Response(serializer.errors, statys=status.HTTP_417_EXPECTATION_FAILED)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, commentId):
    """
        Add a comment to an article
    """

    
    #for this post in the database
    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response(data={'message': 'Comment was not found'}, status=status.HTTP_404_NOT_FOUND)
    
    #extra check to see if the user is the creator of this comment
    if comment.user != request.user:
        return Response(data={'message': 'You are not the creater of this comment'}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment.delete()
    return Response(data={'message': 'Comment was deleted'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_like(request):
    replyId = request.data.get('replyId')
    commentId = request.data.get('commentId')
    articleId = request.data.get('articleId')

    if commentId == None or articleId == None:
        return Response(data={'message': ' bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reaction = Reaction.objects.filter(reply=replyId).filter(comment=commentId).filter(article=articleId).get(user=request.user)  
    except Reaction.DoesNotExist:
        
        try:
            comment = Comment.objects.get(pk=commentId)
            article = BlogArticle.objects.get(pk=articleId)
        except Comment.DoesNotExist:
            return  Response(data={'message': 'wrong request'}, status=status.HTTP_404_NOT_FOUND)
        except BlogArticle.DoesNotExist:
            return Response(data={'message': 'wrong request'}, status=status.HTTP_404_NOT_FOUND)

        try:
            reply = Reply.objects.get(pk=replyId)
        except Reply.DoesNotExist:
            reply = None
        
        reaction = Reaction(user=request.user, article=article, comment=comment,  reply=reply)
    
    reaction.dislike = False
    reaction.like = True
        
    reaction.save()
    reaction_serializer = ReactionSerializer(reaction) 
    return Response(data=reaction_serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_dislike(request):
    replyId = request.data.get('replyId')
    commentId = request.data.get('commentId')
    articleId = request.data.get('articleId')

    if commentId == None or articleId == None:
        return Response(data={'message': ' bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reaction = Reaction.objects.filter(reply=replyId).filter(comment=commentId).filter(article=articleId).get(user=request.user)  
    except Reaction.DoesNotExist:
        
        try:
            comment = Comment.objects.get(pk=commentId)
            article = BlogArticle.objects.get(pk=articleId)
        except Comment.DoesNotExist:
            return  Response(data={'message': 'wrong request'}, status=status.HTTP_404_NOT_FOUND)
        except BlogArticle.DoesNotExist:
            return Response(data={'message': 'wrong request'}, status=status.HTTP_404_NOT_FOUND)

        try:
            reply = Reply.objects.get(pk=replyId)
        except Reply.DoesNotExist:
            reply = None
        
        reaction = Reaction(user=request.user, article=article, comment=comment,  reply=reply)
    
    reaction.dislike = True
    reaction.like = False
        
    reaction.save()
    reaction_serializer = ReactionSerializer(reaction) 
    return Response(data=reaction_serializer.data,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_reaction(request, reactionId):
    try:
        reaction = Reaction.objects.get(pk=reactionId)
    except Reaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    reaction.delete()
    return Response(data={'message': 'reaction was deleted'},status=status.HTTP_200_OK)





    





