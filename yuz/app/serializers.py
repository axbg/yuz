from rest_framework import serializers

from .classes import Photo

class PhotoSerializer(serializers.Serializer):
    original = serializers.CharField()
    cropped = serializers.ListField(child = serializers.CharField())

    def create(self):
        if self.is_valid():
            return Photo(**self.validated_data)
        else:
            raise Exception("Data is not valid")