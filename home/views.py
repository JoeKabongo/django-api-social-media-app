from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET'])
def goHome(request):
    """
        Get comments to a post
    """
    return Response(data={"greeting: Hello world"}, status=status.HTTP_200_OK)