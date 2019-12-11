import io
import cv2
import json
import base64
import logging
import numpy as np

from PIL import Image
from pathlib import Path
from datetime import datetime

from .serializers import OriginalPhotoSerializer
from .classes import Photo

class Logger:
    logging.basicConfig(filename = 'yuz.log', level=logging.INFO)
    logger = logging.getLogger("yuz-logger")

    @staticmethod
    def info(message):
        Logger.logger.info("{} - {}".format(datetime.now(), message))

    @staticmethod
    def warn(message):
        Logger.logger.warn("{} - {}".format(datetime.now(), message))

    @staticmethod
    def error(message):
        Logger.logger.error("{} - {}".format(datetime.now(), message))

class FaceDetector:
    detector = cv2.CascadeClassifier("faces.xml")

    @staticmethod
    def compute_ratio(ix, iy, iw):
        x = int(ix-(iw/2))
        w = int(iw*2)

        if x < 0:
            w += x
            x = 0
        
        h = int(w * 1.25)
        y = int(iy-(h/4))

        if y < 0:
            y = 0

        return x, y, w, h

    @staticmethod
    def prepare_photo(photo_b):
        photo = Photo(photo_b)
        stream = base64.b64decode(photo.get_original())
        cv_image = cv2.cvtColor(np.array(Image.open(io.BytesIO(stream))), cv2.COLOR_BGR2RGB)
            
        faces = FaceDetector.detect(cv_image, 1.4, 3)

        for(x, y, w, h) in faces:
            x, y, w, h = FaceDetector.compute_ratio(x, y, w)
            cropped_face = cv_image[y:y+h, x:x+w]
            _, buffer = cv2.imencode('.jpg', cropped_face)
            photo.add_cropped_photo(base64.b64encode(buffer).decode('utf-8'))        
        return photo

    @staticmethod
    def detect(img, scaleFactor, minNeighbours):
        return FaceDetector.detector.detectMultiScale(img, scaleFactor, minNeighbours)

class ImageTransformer:

    @staticmethod
    def imageToBase64(original):
        return base64.b64encode(original.read())
