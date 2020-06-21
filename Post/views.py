from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.http import HttpResponse, JsonResponse , Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from Account.models import UserAccount
from Comment.models import Reaction
from Comment.serializers import ReactionSerializer
from .models import Post
from .serializers import PostSerializer


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request):
    """
        Allow user to create post
    """

    #extra check if user is authenticated
    try:
        user = request.user
    except:
        Response(data={'error': {'message': 'You are not allowed to take this action'}},status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'POST':
        data = {
            'content': request.data['content'],
            'user':  user.id,
        }
        
        serializer = PostSerializer(data=data)
        
        #make sure the data given to the user is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            #return all the erros if it was not successfull
            return Response(data={'error': {'message': 'unable to process request'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_post(request, postId):
    """
        Delete a post with id=postId
    """

    try:

        post = Post.objects.get(pk=postId)

        #if the user is somehow the author of this post
        if post.user != request.user:
            return Response( 
                        data={'error': {'message' : 'You are not allow to delete this post'}}, 
                        status= status.HTTP_401_UNAUTHORIZED)

        post.delete()
        return Response(data={'message': 'post was deleted'},status=status.HTTP_200_OK)

    #in case the post was not found
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'post was not found'}}, status=status.HTTP_404_NOT_FOUND)

    #other unknown error that may occur
    except:
        return Response(data={'error': {'message': 'Something went wrong'}},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_post(request):
    """
        Edit a post
    """

    #maks sure the request has everything we need
    try:
        user = request.user
        data = {
            'content': request.data['postContent'],
            'postId': request.data['postId'],
            'user':  user.id,
        }
    except:
        return Response(data={'message': 'Something was wrong in your request'}, status=status.HTTP_400_BAD_REQUEST)
   
    #double check that the post exist
    try:
        post = Post.objects.get(pk=data['postId'])
        serializer = PostSerializer(post, data=data)

    except Post.DoesNotExist:
        return Response(data= {'message': 'Post was not found'},status=status.HTTP_404_NOT_FOUND)

    #make sure the user is the author of this post
    if post.user != request.user:
        return Response( 
                    data={'message' : 'You are not allow to edit this post'}, 
                    status= status.HTTP_401_UNAUTHORIZED)
    

    #make sure the data is valid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            data={'message': 'Something was wrong in your request'},
            status=status.HTTP_400_BAD_REQUEST)
    
 

@api_view(['GET'])
def post_detail(request, postId):
    """
    return a specific post, there is no logged in user
    """
    #check the existance of the post
    try:
        post = Post.objects.get(pk=postId)

    except Post.DoesNotExist:
        return Response(data={'message': 'post was not found'}, status=status.HTTP_404_NOT_FOUND)

    post_serializer = PostSerializer(post)
    data = [post_serializer.data, []]
    
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail_user_reaction(request, postId, username):
    """
    return a specific post and if the current user liked or disliked the post
    """
    #check the existance of the post
    print(request.user.username)
    try:
        post = Post.objects.get(pk=postId)

    except Post.DoesNotExist:
        return Response(data={'message': 'post was not found'}, status=status.HTTP_404_NOT_FOUND)

    
    post_serializer = PostSerializer(post)
    data = post_serializer.data

    #[post_detail, reactionId]
    lists = [data, -1]
    
    #found out if this user liked this post
    try:
        reaction  = Reaction.objects.filter(comment__isnull=True).filter(reply__isnull=True).filter(user=request.user).get(post=post)
        data['isLiked'] = reaction.like
        data['isDisliked'] = reaction.dislike  
        lists[1] = reaction.id
    except Reaction.DoesNotExist:
        pass  
    return Response(data=lists, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_list(request):
    """
    return all the posts
    """
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    data_list = [serializer.data, []]

    return Response(data=data_list, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_list_user_reactions(request):
    """
    return all the posts and user reactions to it
    """
    posts = Post.objects.all()
    post_serializer = PostSerializer(posts, many=True)


    reactions = Reaction.objects.filter(article__isnull=True).filter(reply__isnull=True).filter(comment__isnull=True).filter(user=request.user)
    reaction_serialzer = ReactionSerializer(reactions, many=True)

    data_list = [post_serializer.data, reaction_serialzer.data]

    return Response(data=data_list, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request, postId):
    """
        User likes a post with id=postId
    """

    #double check the post exisit
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(data={'message': 'post does not exisit'}, status=status.HTTP_404_NOT_FOUND)
    
    #found out if there is already a reaction where this user liked or disliked the post, if not create a new one
    try:
        reaction = Reaction.objects.filter(article__isnull=True).filter(comment__isnull=True).filter(reply__isnull=True).filter(user=request.user).get(post=post)
    except:
        reaction = Reaction(post=post, user=request.user)

    reaction.like = True
    reaction.dislike = False
    reaction.save()
    
    reaction_serializer = ReactionSerializer(reaction)

    
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dislike_post(request, postId):
    """
        User dislikes a post with id=postId
    """
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(data={'message': 'post does not exisit'}, status=status.HTTP_404_NOT_FOUND)
    
    #found out if there is already a reaction where this user liked or disliked the post, if not create a new one
    try:
        reaction = Reaction.objects.filter(article__isnull=True).filter(comment__isnull=True).filter(reply__isnull=True).filter(user=request.user).get(post=post)
    except:
        reaction = Reaction(post=post, user=request.user)

    reaction.like = False
    reaction.dislike = True
    reaction.save()
    reaction_serializer = ReactionSerializer(reaction)
    
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_reaction(request, reactionId):
    """
        when user unlike or undislike a post
    """
    try:
        reaction = Reaction.objects.get(pk=reactionId)
    except Reaction.DoesNotExist:
        return Response(data={"message": 'bad request, reaction not found'}, status=status.HTTP_404_NOT_FOUND)
    
    reaction.delete()
    return Response(data={'message': 'reaction was deleted'}, status=status.HTTP_200_OK)



