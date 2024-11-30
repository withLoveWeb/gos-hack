from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from user.serializer import RegisterSerializer



class RegisterView(APIView):
    permission_classes = []

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        refresh_token = response.data.get('refresh', None)
        access_token = response.data['access']
        
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


class CustomTokenRefreshView(TokenRefreshView):
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
