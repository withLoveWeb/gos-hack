from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from route.serializer import RouteSerializer

class RouteInfoView(APIView):

    @swagger_auto_schema(request_body=RouteSerializer)
    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data, flush=True)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPlaceView(APIView):

    @swagger_auto_schema(request_body=RouteSerializer)
    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data, flush=True)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

