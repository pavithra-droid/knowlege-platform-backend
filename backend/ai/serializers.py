from rest_framework import serializers

class AIQuerySerializer(serializers.Serializer):
    question = serializers.CharField()