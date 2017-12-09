from rest_framework import serializers


class SearchResultSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
