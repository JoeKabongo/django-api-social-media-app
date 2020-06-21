from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes


from Post.models import Post
from .models import Comment, Reply, Reaction
from BlogPost.models import BlogArticle
from .serializers  import CommentSerializer, ReplySerializer, ReactionSerializer


# Create your views here.


@api_view(['GET'])
def get_post_comments(request, postId):
    """
        Get comments to a post
    """
    comment = Comment.objects.filter(post=postId)
    serializer = CommentSerializer(comment, many=True)

    data = [serializer.data, []]
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_comments_user_reactions(request, postId):
    """
        Get comments to a post, and user reactions(like and dislike)
    """
    comment = Comment.objects.filter(post=postId)
    comment_serializer = CommentSerializer(comment, many=True)

    post = Post.objects.get(pk=postId)
    reactions = Reaction.objects.filter(post=post).filter(user=request.user)
    reaction_serializer = ReactionSerializer(reactions, many=True)

    data = [comment_serializer.data, reaction_serializer.data]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_article_comments(request, articleId):
    """
        Get comments to an article
    """
    comment = Comment.objects.filter(article=articleId)
    serializer = CommentSerializer(comment, many=True)

    data = [serializer.data, []]
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def article_comments_user_reactions(request, articleId):
    """
        Get comments to an article and user reactions to comments
    """
    comment = Comment.objects.filter(article=articleId)
    serializer = CommentSerializer(comment, many=True)

    article = BlogArticle.objects.get(pk=articleId)
    reactions = Reaction.objects.filter(reply__isnull=True).filter(user=request.user).filter(article=article)

    reaction_serializer = ReactionSerializer(reactions, many=True)

    data = [serializer.data, reaction_serializer.data]
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_comment(request):
    """
        Save a comment
    """ 

    #get all the data associated with the request
    try:
        data ={
            'post' : request.data.get('postId'),
            'article': request.data.get('articleId'),
            'user' : request.user.id,  
            'content' : request.data['content']
        }
    except:
        return Response(data={'message': 'Something was wrong in your request'}, status=status.HTTP_400_BAD_REQUEST)
    

    comment_serializer = CommentSerializer(data=data)

    #make sure the data provided is compatible with the comment serializer
    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(data=comment_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_comment(request, commentId):
    """
        Edit a comment
    """
    try:
        data = {
            'content': request.data['content'],
            'commentId': commentId,
            'user': request.user.id
        }
    
    except :
        return Response(data={'error': {'message': 'Bad request'}}, status=status.HTTP_400_BAD_REQUEST)
   

    #make sure the comment exisit
    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
       return Response(data={'error': {'message': 'Comment was not found'}}, status=status.HTTP_404_NOT_FOUND)

    #extra check to make sure this comment is associated with our user
    if comment.user != request.user:
        return Response(
            data={'error': {'message': 'You are not authorized to edit this post'}}, 
            status=status.HTTP_401_UNAUTHORIZED )

    serializer = CommentSerializer(comment, data=data)

  
        
    
    #make sur the serializer is valid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #for some reasons the serializer was not valid
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, commentId):
    """
        Edit a comment
    """
    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response(data={'message': 'comment was not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if comment.user == request.user.id:
        return Response(data={'message': 'You cannot delete this comment'}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment.delete()
    return Response(data={'message': 'comment was deleted'}, status=status.HTTP_200_OK)

@api_view(['GET'])

def get_replies_to_comment(request, commentId):
    """
        get replies to a comment
    """
    replies = Reply.objects.filter(parentComment=commentId)
    serializer = ReplySerializer(replies, many=True)

    data = [serializer.data, []]
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def replies_to_comment_user_reactions(request, commentId):
    """
        get replies to a comment and user reactions to those replies if any
    """
    replies = Reply.objects.filter(parentComment=commentId)
    replies_serializer = ReplySerializer(replies, many=True)

    comment = Comment.objects.get(pk=commentId)
    reactions = Reaction.objects.filter(reply__isnull=False).filter(user=request.user).filter(comment=comment)

    reaction_serializer = ReactionSerializer(reactions, many=True)

    data = [replies_serializer.data, reaction_serializer.data]
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def save_reply(request, articleId, postId, commentId):
    """
        save a reply
    """
    try:
        data ={
            'content' : request.data['content'],
            'parentComment' : commentId,
            'user': request.user.id,
        }

        #see which parent it is for the reply either article or post
        if int(articleId) != -1:
            data['article'] = articleId

        if int(postId) != -1:
            data['post'] = int(postId)
        

    except:
        return Response(data={'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
    
    #make sure that data provided is valid
    reply_serializer = ReplySerializer(data=data)
    if reply_serializer.is_valid():
        reply_serializer.save()
        return Response(data=reply_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(reply_serializer.errors)
        return Response(data={'message': 'Something was wrong in your request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_reply(request, replyId):
    """
        Edit a reply
    """
    try:
        data = {
            'content': request.data['content'],
            'user': request.user.id,
            'parentComment': request.data['commentId']
        }
    
    except :
        return Response(data={'error': {'message': 'Bad request'}}, status=status.HTTP_400_BAD_REQUEST)
   

    #make sure the comment exisit
    try:
        reply = Reply.objects.get(pk=replyId)
    except Reply.DoesNotExist:
       return Response(data={'error': {'message': 'Comment was not found'}}, status=status.HTTP_404_NOT_FOUND)

    #extra check to make sure this comment is associated with our user
    if reply.user != request.user:
        return Response(
            data={'error': {'message': 'You are not authorized to edit this reply'}}, 
            status=status.HTTP_401_UNAUTHORIZED )

    serializer = ReplySerializer(reply, data=data)

      
    #make sur the serializer is valid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    #for some reasons the serializer was not valid
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_reply(request, replyId):
    """
        Delete a reply
    """
    try:
        reply = Reply.objects.get(pk=replyId)
    except ReplyDoesNotExist:
        return Response(data={'message': 'reply was not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if reply.user != request.user:
        return Response(data={'message': 'You cannot delete this reply'}, statuts=status.HTTP_401_UNAUTHORIZED)
    
    reply.delete()

    return Response(data={'message': 'reply has been deleted'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_comment(request, articleId, postId, commentId):
    """
        Like a comment whose id = commentId and whose parent post is postId
    """
    articleId = int(articleId)
    postId = int(postId)
    commentId = int(commentId)
    
    if articleId == -1 and postId == -1:
        return Response(data={'message': 'wrong request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        print('comment not found')
        return Response(data={'message': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if articleId == -1:
        article = None
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            print('post not found')
            return Response(data={'message': 'post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        post = None
        try:
            article = BlogArticle.objects.get(pk=articleId)
        except BlogArticle.DoesNotExist:
            print('artice not found')
            return Response(data={'message': 'article not found'}, status=status.HTTP_404_NOT_FOUND)
        

    
     #found out if there is already a reaction where this user liked or disliked the post, if not create a new one
    try:
        if post == None:
            reaction = Reaction.objects.filter(reply__isnull=True).filter(post__isnull=True).filter(article=article).get(comment=comment)
        
        else:
            reaction = Reaction.objects.filter(reply__isnull=True).filter(article__isnull=True).filter(post=post).get(comment=comment)


    except Reaction.DoesNotExist:
        reaction = Reaction(comment=comment, user=request.user, post=post, article=article)
    
    reaction.like = True
    reaction.dislike = False 
    reaction.save()

    reaction_serializer = ReactionSerializer(reaction)
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dislike_comment(request, articleId, commentId, postId):
    """
    Dislike a comment
    """

    articleId = int(articleId)
    postId = int(postId)
    commentId = int(commentId)
    
    #make sure a comment or post is is valid
    if articleId == -1 and postId == -1:
        return Response(data={'message': 'wrong request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        print('comment not found')
        return Response(data={'message': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if articleId == -1:
        article = None
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(data={'message': 'post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        post = None
        try:
            article = BlogArticle.objects.get(pk=articleId)
        except BlogArticle.DoesNotExist:
            return Response(data={'message': 'article not found'}, status=status.HTTP_404_NOT_FOUND)
        

    
    #found out if there is already a reaction where this user liked or disliked the post, if not create a new one
    try:
        if post == None:
            reaction = Reaction.objects.filter(reply__isnull=True).filter(post__isnull=True).filter(article=article).get(comment=comment)
        
        else:
            reaction = Reaction.objects.filter(reply__isnull=True).filter(article__isnull=True).filter(post=post).get(comment=comment)


    except Reaction.DoesNotExist:
        reaction = Reaction(comment=comment, user=request.user, post=post, article=article)
    
    reaction.like = False
    reaction.dislike = True 
    reaction.save()

    reaction_serializer = ReactionSerializer(reaction)
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_reply(request, commentId, replyId):
    """
        Like a reply
    """
    #make sure the replyId and comment id is valid
    try:
        reply = Reply.objects.get(pk=replyId)
        comment = Comment.objects.get(pk=commentId)
    except Reply.DoesNotExist:
        return Response(data={'message': 'reply was not found'}, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExisit:
        return Response(data={'message': 'comment was not found'}, status=status.HTTP_404_NOT_FOUND)

    #found out if the user have liked or disliked this reply, avoiding doing more than one reaction
    try:
        reaction = Reaction.objects.filter(user=request.user).filter(comment=comment).get(reply=reply)
    except:
        reaction = Reaction(reply=reply, comment=comment, user=request.user)
    
    #update the old or new reaction
    reaction.like = True
    reaction.dislike = False 
    reaction.save()

    reaction_serializer = ReactionSerializer(reaction)
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dislike_reply(request, commentId, replyId):
    """
        dislike a reply
    """

    #make sure the replyId and comment id is valid
    try:
        reply = Reply.objects.get(pk=replyId)
        comment = Comment.objects.get(pk=commentId)
    except Reply.DoesNotExist:
        return Response(data={'message': 'reply was not found'}, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExisit:
        return Response(data={'message': 'comment was not found'}, status=status.HTTP_404_NOT_FOUND)

    #found out if the user have liked or disliked this reply, avoiding doing more than one reaction
    try:
        reaction = Reaction.objects.filter(user=request.user).filter(comment=comment).get(reply=reply)
    except:
        reaction = Reaction(reply=reply, comment=comment, user=request.user)
    
    #update the old or new reaction
    reaction.dislike = True 
    reaction.like = False
    reaction.save()

    reaction_serializer = ReactionSerializer(reaction)
    return Response(reaction_serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_reaction(request, reactionId):
    """
        Remove an like/dislike to a comment or reply
    """   

    try:
        reaction = Reaction.objects.get(pk=reactionId)
    except Reaction.DoesNotExist:
        return Response(data={'message': 'reaction not found'}, status=status.HTTP_404_NOT_FOUND)
    
    reaction.delete()
    return Response(data={'message' : 'reaction was deleted'}, status=status.HTTP_200_OK)
   


    