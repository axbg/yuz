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
            
            #extract faces
            faceDetector = cv2.CascadeClassifier('faces.xml')
            faces = faceDetector.detectMultiScale(cv_image, 1.1, 4)

            for(x, y, w, h) in faces:
                cv2.rectangle(cv_image, (int(x-(w/2)), int(y-(h/4))), (int(x+w+w/2), int(y+h*2)), (255, 0, 0), 2)
                # cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            _, buffer = cv2.imencode('.jpg', cv_image)
            photo.add_cropped_photo(base64.b64encode(buffer).decode('utf-8'))
            return Response(CroppedPhotoSerializer(photo).data)
        except Exception as e:
            print(e)
            return Response({"message": "nasty error happened"}, status=500)