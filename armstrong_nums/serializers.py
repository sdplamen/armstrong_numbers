from rest_framework import serializers

class ArmstrongNumberSerializer(serializers.Serializer):
    start_range = serializers.IntegerField(min_value=0)
    end_range = serializers.IntegerField(min_value=0)

    def validate(self, data):
        if data['start_range'] > data['end_range']:
            raise serializers.ValidationError('End range must be greater than or equal to start range.')
        return data