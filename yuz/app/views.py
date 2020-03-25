import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .classes import Photo
from .serializers import CroppedPhotoSerializer
from .utils import FaceDetector, ImageTransformer
from .utils import Logger


class RootView(APIView):
    def get(self, request):
        Logger.info("RootView - GET")
        return Response({"message": "yuz back-end"})


class RegisterView(APIView):
    def post(self, request):
        Logger.info("RegisterEndpoint - POST")
        data = json.loads(request.body)

        try:
            assert "username" in data and data["username"] != "", "username missing from request"
            assert "password" in data and data["password"] != "", "password missing from request"
            assert "email" in data and data["email"] != "", "email missing from request"
            assert len(data["password"]) > 8, "password should have at least 8 characters"
            assert "@" in data["email"] and "." in data["email"] and len(data["email"]) > 11, "invalid email"
            assert len(User.objects.filter(
                Q(username=data["username"]) | Q(email=data["email"]))) == 0, "username or email already registered"
        except AssertionError as ae:
            return Response({"message": ae.args[0]}, status=400)

        User.objects.create_user(**data)
        return Response({"message": "Registered"})


class ExtractorEndpoint(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Logger.info("ExtractorEndpoint - POST")
        try:
            original = request.data['original']

            if type(original) == InMemoryUploadedFile:
                original = ImageTransformer.imageToBase64(original)

            photo = FaceDetector.prepare_photo(original)
            return Response(CroppedPhotoSerializer(photo).data)
        except Exception as e:
            print(e)
            return Response({"message": "nasty error happened"}, status=500)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Logger.info("Logout - {}".format(request.user))
        request.user.auth_token.delete()
        return Response({"message": "Token was removed"})


@method_decorator(csrf_exempt, name='dispatch')
class WebView(APIView):
    get_template = None
    post_template = None

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template)

    def post(self, request, *args, **kwargs):
        try:
            assert 'Origin' in request.headers, "Origin missing or not valid"
            formatted_photo = Photo(None)
            for image in request.data.items():
                base64 = ImageTransformer.imageToBase64(image[1])
                processed_photos = FaceDetector.prepare_photo(base64)
                for processed_photo in processed_photos.get_cropped():
                    formatted_photo.add_cropped_photo(processed_photo)
        except AssertionError as e:
            return Response({"message": e.args[0]}, status=400)
        return Response(CroppedPhotoSerializer(formatted_photo).data)
