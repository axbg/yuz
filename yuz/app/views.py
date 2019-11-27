import io
import cv2
import json
import base64
import numpy as np

from PIL import Image
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import Logger
from .classes import Photo
from .utils import FaceDetector
from .serializers import OriginalPhotoSerializer, CroppedPhotoSerializer


class RootEndpoint(APIView):
    def get(self, request):
        Logger.info("RootEndpoint - GET")
        return Response({"message": "yuz back-end"})


class ExtractorEndpoint(APIView):
    def post(self, request):
        Logger.info("ExtractorEndpoint - POST")
        try:
            photo = OriginalPhotoSerializer(data=json.loads(request.body)).create()
            stream = base64.b64decode(photo.get_original())
            cv_image = cv2.cvtColor(np.array(Image.open(io.BytesIO(stream))), cv2.COLOR_BGR2RGB)
            
            faces = FaceDetector.detect(cv_image, 1.05, 6)

            for(x, y, w, h) in faces:
                cropped_face = cv_image[int(y-(h/4)):int(y+h*2), int(x-(w/2)):int(x+w*1.5)]
                _, buffer = cv2.imencode('.jpg', cropped_face)
                photo.add_cropped_photo(base64.b64encode(buffer).decode('utf-8'))

            return Response(CroppedPhotoSerializer(photo).data)
        except Exception as e:
            print(e)
            return Response({"message": "nasty error happened"}, status=500)