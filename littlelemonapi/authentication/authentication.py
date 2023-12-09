from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'Username or email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create a response with user details and tokens
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'groups': [group.name for group in user.groups.all()],
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        return response


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = None

        if username:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Create a response with user details and tokens
            response_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'groups': [group.name for group in user.groups.all()],
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            response.set_cookie(key='access_token', value=access_token, httponly=True)
            return response
        else:
            # Both authentication attempts failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'groups': [group.name for group in user.groups.all()],
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

        # Set cookies to expire in the past
        response.set_cookie('access_token', '', expires=timezone.now() - timedelta(days=1), httponly=True)
        response.set_cookie('refresh_token', '', expires=timezone.now() - timedelta(days=1), httponly=True)

        return response

