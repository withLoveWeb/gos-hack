from rest_framework import serializers

class RouteSerializer(serializers.Serializer):
    start_latitude = serializers.FloatField(
        required=True, 
        min_value=-90.0, 
        max_value=90.0, 
        help_text="Широта начала"
    )
    start_longitude = serializers.FloatField(
        required=True, 
        min_value=-180.0, 
        max_value=180.0, 
        help_text="Долгота начала"
    )
    end_latitude = serializers.FloatField(
        required=True, 
        min_value=-90.0, 
        max_value=90.0, 
        help_text="Широта конца"
    )
    end_longitude = serializers.FloatField(
        required=True, 
        min_value=-180.0, 
        max_value=180.0, 
        help_text="Долгота конца"
    )

    def validate(self, attrs):
        start_coords = (attrs['start_latitude'], attrs['start_longitude'])
        end_coords = (attrs['end_latitude'], attrs['end_longitude'])

        if start_coords == end_coords:
            raise serializers.ValidationError(
                "Начальная и конечная точки маршрута не могут совпадать."
            )
        return attrs

