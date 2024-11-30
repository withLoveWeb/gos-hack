from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Получаем токен из cookies
        token = request.COOKIES.get('access_token')

        if not token:
            raise AuthenticationFailed('No token found in cookies')

        # Если токен найден, передаем его в аутентификацию
        # Теперь вызовим базовый метод authenticate с этим токеном
        validated_token = self.get_validated_token(token)
        print(validated_token, flush=True)

        return self.get_user(validated_token), validated_token
