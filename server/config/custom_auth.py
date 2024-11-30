from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from captain.models import Captain

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('No token found in cookies')

        validated_token = self.get_validated_token(token)

        return self.get_user(validated_token), validated_token


class CaptainAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('login')
        password = request.data.get('password')

        if not email or not password:
            return None

        try:
            captain = Captain.objects.get(email=email)
        except Captain.DoesNotExist:
            raise AuthenticationFailed('Captain not found')

        if not captain.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        return (captain, None)

class CaptainJWTAuthentication(JWTAuthentication):

