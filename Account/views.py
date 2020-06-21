#imports from django
from django.http import HttpResponse, JsonResponse , Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

#imports from rest_framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#import objects from app
from .models import UserAccount, UpdatePasswordToken
from Comment.models import Reaction
from Comment.serializers import ReactionSerializer
from .serializers import AccountRegistrationSerializer, AccountSerializer

#import cloudinary for storing image
import cloudinary
import cloudinary.uploader
import cloudinary.api


import string
import random


def get_random_token(length):
    """
        Generate a random string, if length characters
    """
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    token = ""
    for i in range(length):
        index = random.randint(0, len(characters) - 1)
        token += characters[index]
    
    return token

def send_password_token(email, new_token):
    subject = 'NbaTalk | Reset password '
    message = 'Use this pin: '+ new_token + 'to reset your password. It will expires in 15 mins'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )
    print("sending email hahahahaha")

    
@api_view(['POST', ])
def request_password_update(request):
    """
        This endpoint takes in a email and check if a user with that email exist.
        If the user exist, send an email with a pin
    """

    #make sure the request has an email attached 
    try:
        user_email = request.data['userEmail']
    except KeyError:
        return Response(data={'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    #if a user with this email is found
    try:
        user = UserAccount.objects.get(email=user_email)
        #make sure user that not have an update token, if it has remove it
        try:
            password_token = UpdatePasswordToken.objects.get(user=user)
        except:
            password_token = UpdatePasswordToken(
                user=user,
                token=''
            )

        #generate new token and send email with the token
        new_token = get_random_token(10)
        password_token.token = new_token
        password_token.save()

        try:
            send_password_token(user_email, new_token)
        except:
            return Response(data={'success': False, 'message': 'Something went wrong'}, status=status.HTTP_417_EXPECTATION_FAILED)

        #return a success message
        return Response(data={'success': True, 'message': 'Email have been said to user'}, status=status.HTTP_200_OK)


    except UserAccount.DoesNotExist:
        return Response(data={'success': False ,'message': 'User was not found'}, status=status.HTTP_404_NOT_FOUND)
        #just return a failure message


@api_view(['POST'])
def confirm_user_passcode(request):
    try:
        user_email = request.data['userEmail']
        passcode = request.data['passcode']
    except:
        return Response(data={"message": 'This is a bad reqeust'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        current_user = UserAccount.objects.get(email=user_email)
    except UserAccount.DoesNotExist:
        return Response(data={'message': 'User was not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        password_token = UpdatePasswordToken.objects.get(user=current_user)
        if password_token.token == passcode:
            password_token.delete()
            return Response(data={'success': True, 'message':'passcode was valid'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'passcode did not match'}, status=status.HTTP_401_UNAUTHORIZED)

    except UpdatePasswordToken.DoesNotExist:
        return Response(data={'message': 'User did not have a passcode'}, status=status.HTTP_401_UNAUTHORIZED)

    


    
@api_view(['PUT', ])
def reset_password(request):
    """
        Reset password of user
    """
    print("we are here")
    try:
        new_password = request.data['newPassword']
        email = request.data['email']
    except KeyError:
        return Response(data={'message': 'This was an invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        current_user = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return Response(data={'message': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    current_user.set_password(new_password)
    current_user.save()

    token, _ = Token.objects.get_or_create(user=current_user)


    data ={
        'isWriter': current_user.isWriter,
        'username': current_user.username,
        'token': token.key
    }

    return Response(data=data, status=status.HTTP_200_OK)




#cloudinary cloud where images are stored
@api_view(['GET', ])
def user_detail_view(request, username):
    """
        Return the detail of user 
    """
    
    #make user username exist
    try:
        user = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        newdict = {'not_found': True}
        return Response(data={'error': {'message': 'user not found'}}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(user)
    data_list = [serializer.data, []]
    return Response(data=data_list, status=status.HTTP_200_OK)


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail_view_reactions(request, username):
    """
        Return the detail of user 
    """
    #make user username exist
    try:
        user = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
        newdict = {'not_found': True}
        return Response(data={'error': {'message': 'user not found'}}, status=status.HTTP_404_NOT_FOUND)

    account_serializer = AccountSerializer(user)


    reactions = Reaction.objects.filter(article__isnull=True).filter(reply__isnull=True).filter(comment__isnull=True).filter(user=request.user)
    reaction_serialzer = ReactionSerializer(reactions, many=True)

    data_list = [account_serializer.data, reaction_serialzer.data]
    return Response(data=data_list, status=status.HTTP_200_OK)
    
    
    
@api_view(['POST',])
def registration_view(request):
    """
        Funtion that register the user using. User is registerd and a token is created for that user
        Users data are sent back to the client
    """
    data = JSONParser().parse(request)
    serializer = AccountRegistrationSerializer(data=data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data = {
            'success': "successfully registered a new user",
            'user_id': new_user.id,
            'token': Token.objects.get(user=new_user).key,
            'username': new_user.username,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)   
     
    data = serializer.errors
    return Response(data)


#login a user
@api_view(['POST', ])
def login_view(request):
    """
        Login a user
    """
    #make sure the request have the data needed
    data = request.data
    try:
        username = data["usernameOrEmail"]
        password = data["password"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    #check if a user with such username or email exist
    try:
        user = UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:

        try:
            user = UserAccount.objects.get(email=username)
            username=user.username
        except  UserAccount.DoesNotExist:
            return Response({'error': 'Such user was not found'},
                        status=status.HTTP_404_NOT_FOUND)
    
    #check to see if username with that password exist
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

    #return info of the user
    token, _ = Token.objects.get_or_create(user=user)
    data = {
        "success": True,
        "token": token.key,
        "username": user.username,
        "date_joined": user.date_joined,
        "email" : user.email,
        "isWriter": user.isWriter,
    }
    return Response(data=data, status=status.HTTP_200_OK)



 

@api_view(['PUT', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_detail_view(request):
    """
        Update the authenticated user information
    """

    #extra check if user is authenticated
    try:
        user = request.user
    except:
        Response(status=status.HTTP_400_BAD_REQUEST)

    if request.data.get('profileImage') != None :
        images = cloudinary.uploader.upload(request.data['profileImage']).get('url').split("/")
        n = len(images)
        profileImage = ''
        index = 0
        # circle the image for the profile
        while index < n:
            if index == len(images) - 1:
                profileImage += 'g_face,r_max/'
                profileImage += images[index]
            elif images[index] == 'upload':
                profileImage += 'upload/'
                index +=1
            else:
                profileImage += images[index] + "/"
            
            index += 1
        
        # for index, string in enumerate(image):
        #     if index == len(image) - 1:
        #         profileImage += 'g_face,r_max/'
        #         profileImage += string
        #     else:
        #         profileImage += string + "/"
        
        print(profileImage)
        
        

    else:
        profileImage = request.user.profileImage

    user_data = {
        'username' : request.data['username'],
        'email' : request.data['email'],
        'bio' : request.data['bio'],
        'profileImage' : profileImage
    }


    #update was successull
    serializer = AccountSerializer(user, data=user_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    #return all the erros if it was not successfull
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
def user_list_view(request):
    """
     View list of all the users
    """
    user = UserAccount.objects.all()
    serializer = AccountSerializer(user, many=True)
    return Response(serializer.data)



