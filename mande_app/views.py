from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth.decorators import login_required

# Component: login_test
# Description: View - Endpoint that serves as a test for token-authentication
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

# This endpoint should be accessed via token-authentication, using commands like:
# curl -X POST -H "Authorization: Token <token>" http://localhost:8000/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login_test(request):
    return HttpResponse(f"You are logged-in as {request.user}");
