from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import (
    NewspaperJournalist,
    NewspaperPerson,
    NewspaperSheet
)

# Create your views here.
class DataUploadEndpoint(APIView):
    def post(self, request):
        """
            Upload data sent as JSON
        """
        print(request.data)
        Response({"message": "Got some data!",})
