from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import Logger
from .classes import Photo
from .serializers import PhotoSerializer


class RootEndpoint(APIView):
    def get(self, request):
        Logger.info("RootEndpoint - GEt")
        return Response({"message": "yuz back-end"})