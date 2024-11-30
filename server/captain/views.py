from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from config.custom_auth import CaptainAuthentication, CaptainJWTAuthentication
from captain.models import Captain
from captain.serializer import CaptainSerializer, CaptainLoginSerializer 



class RegisterCaptainView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=CaptainSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CaptainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Капитан успешно зарегистрирован!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaptainLogoutView(APIView):
    authentication_classes = [CaptainJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CaptainProfileView(APIView):
    authentication_classes = [CaptainJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("test", flush=True)

        if not isinstance(request.user, Captain):
            return Response(
                {"detail": "Access forbidden: User is not a captain."},
                status=403
            )
        return Response({
            "id": request.user.id, 
            "email": request.user.email,
            "name": request.user.name,
            "surname": request.user.surname,
            "lastname": request.user.lastname,
            "phone_number": request.user.phone_number,
            "rate": request.user.rate,
            # "avatar_url": request.user.avatar.photo.url if request.user.avatar else None,
        })


class CaptainAuthView(APIView):
    authentication_classes = [CaptainAuthentication]

    @swagger_auto_schema(request_body=CaptainLoginSerializer)
    def post(self, request):
        user = request.user
        if user:
            refresh = RefreshToken.for_user(user)
            refresh['id'] = user.id

            refresh_token = refresh
            access_token = refresh.access_token

            response = Response(
                { 
                    "refresh": str(refresh_token), 
                    "access": str(access_token) 
                }
            )

            response.set_cookie(
                'refresh_token', refresh_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=3600 * 24 * 7
            )
            response.set_cookie(
                'access_token', access_token,
                httponly=True,  
                secure=True,  
                samesite='Strict',
                max_age=3600  
            )

            return response

        return Response({"error": "Invalid credentials"}, status=400)


class CaptainTokenRefreshView(TokenRefreshView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('No refresh token found in cookies')

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({
                'access': access_token
            })
            response.set_cookie(
                'access_token', access_token, 
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=3600
            )
            return response

        except Exception as e:
            raise AuthenticationFailed(f'Failed to refresh token: {str(e)}')


