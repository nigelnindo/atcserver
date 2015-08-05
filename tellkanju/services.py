from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth

import random, string 
import dropbox

from rest_framework import serializers, exceptions


from .models import Report

DROPBOX_TOKEN = 'EkWn4WUf7O8AAAAAAAApwu_d1RGtnQIwdOZZynQaLcCByUupg_4OiigluVtpknLg' #token to be used to make requests to DropBox

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class ReportSerializerPublic(serializers.ModelSerializer):
 	class Meta:
 		model = Report
 		fields = ('id_number','description','reportedImage','latitude','longitude')#fill in these fields

def test_image_path(filename):
	return '/testImages/{0}{1}'.format(randomword(5),filename)


class MyReport:

	def __init__(self):
		self.viewset = Report.objects.all()

	def get_all_details(self):
		return self.viewset

	@staticmethod
	def get_public_serializer():
		return ReportSerializerPublic

	def get_all_reports(self):
		multiple_instances = self.get_all_details()
		return multiple_instances

	def upload_new_report(self,data):
		serializer_class = MyReport.get_public_serializer()
		serialized_data = serializer_class(data=data)
		if serialized_data.is_valid():
			thisDict = data.dict()
			reportedImage = thisDict['reportedImage']
			client = dropbox.client.DropboxClient(DROPBOX_TOKEN)
			response = client.put_file(test_image_path(filename=reportedImage.name),reportedImage)
			print response
			Report.objects.create(id_number=thisDict['id_number'],
				description=thisDict['description'],
				reportedImage=thisDict['reportedImage'],
				latitude=thisDict['latitude'],
				longitude=thisDict['longitude'])
			print 'Success uploading Image'	
			return 'upload:success'
		else:
			print serialized_data.errors
			raise exceptions.ParseError(detail=serialized_data.errors)	














