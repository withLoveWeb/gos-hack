import os
import pandas as pd

from pytz import timezone
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from alg.main import get_schedule
from route.serializer import RouteSerializer, RouteScheduleSerializer

class RouteInfoView(APIView):

    @swagger_auto_schema(request_body=RouteSerializer)
    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data, flush=True)

            
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RouteScheduleView(APIView):

    @swagger_auto_schema(request_body=RouteScheduleSerializer)
    def post(self, request):
        serializer = RouteScheduleSerializer(data=request.data)
        
        print(request.data, flush=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            # Извлечение параметров из сериализатора
            latitude = validated_data['start_latitude']
            longitude = validated_data['start_longitude']
            dock_end = validated_data['bertch_name']
            
            # Определение текущего времени
            tz = timezone('Europe/Moscow')
            datetime_cur = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')

            sch_path = os.path.join('alg', 'schedule.csv')
            mr_path = os.path.join('alg', 'moorings.csv')
            
            try:
                schedule_df = get_schedule(sch_path, mr_path, latitude, longitude, dock_end, datetime_cur)
                schedule_json = schedule_df.to_dict(orient='records')
                return Response(schedule_json, status=status.HTTP_200_OK)
            except FileNotFoundError as e:
                return Response({'error': f'File not found: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OrderPlaceView(APIView):

    @swagger_auto_schema(request_body=RouteSerializer)
    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data, flush=True)

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

