from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the cookie
        token = request.COOKIES.get('access_token')
        if not token:
            # No token in the cookie, return None to allow unauthenticated access
            return None

        # Validate the token
        jwt_authentication = JWTAuthentication()
        try:
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
            return (user, validated_token)
        except AuthenticationFailed:
            # In case of token validation failure, return None
            # This allows endpoints with permission_classes = [AllowAny] to be accessed
            return None


