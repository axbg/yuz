from rest_framework import serializers

from .classes import Photo

class OriginalPhotoSerializer(serializers.Serializer):
    original = serializers.CharField()

    def create(self):
        if self.is_valid():
            return Photo(**self.validated_data)
        else:
            raise Exception("Data is not valid")

class CroppedPhotoSerializer(serializers.Serializer):
    cropped = serializers.ListField(child = serializers.CharField(), source='_cropped')