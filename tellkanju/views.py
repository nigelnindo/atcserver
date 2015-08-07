from django.shortcuts import render
from django.contrib.auth.models import User 
from django.contrib import auth
from django.db import IntegrityError

from rest_framework import exceptions
from rest_framework.views import APIView, Response, status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .services import MyReport

# Create your views here.

class ViewAllReports(APIView):
	def get(self,request,format=None):
		myreport = MyReport()
		serializer_class = MyReport.get_public_serializer()
		serialized_data = serializer_class(myreport.get_all_details(),many=True)
		return Response(serialized_data.data)

class UploadReport(APIView):
	def post(self,request,format=None):
		myreport = MyReport()
		return Response(myreport.upload_new_report(data=request.data))

class TryToken(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request,format=None):
		return Response(request.user.username)