from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Extract the refresh token from the cookie
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # Generate new access and refresh tokens
        data = serializer.validated_data

        # Create response with new access token
        response = Response(data, status=status.HTTP_200_OK)

        # Set new access token in cookies
        response.set_cookie(key='access_token', value=data['access'], httponly=True)

        # Optionally, set a new refresh token in cookies if you are also rotating refresh tokens
        if 'refresh' in data:
            response.set_cookie(key='refresh_token', value=data['refresh'], httponly=True)

        return response
