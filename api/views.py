from django.shortcuts import render
from django.contrib.auth.models import User 
from django.contrib import auth
from django.db import IntegrityError

from rest_framework import exceptions
from rest_framework.views import APIView, Response, status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from .models import UserProfile

from .services import MyUserProfile, MyQuestion, MyQuestionComment, MyUserProfileImage


class ActionUserSignUp(APIView):
	def post(self, request, format=None):
		print('We are at class signup!!!')
		print(request.data)
		try:
			thisDict = request.data.dict()
			print('We converted from querydict')
		except AttributeError:
			thisDict = request.data
		print(thisDict['username'])
		print(thisDict['password'])
		try:
			print(thisDict['description'])
			user = User.objects.create_user(username=thisDict['username'],password=thisDict['password'])
			UserProfile.objects.create(user_relation=user,description=thisDict['description'])
			return Response('signup:successful')
		except KeyError:
			print('Key Error.')
			raise exceptions.ParseError(detail='Provide all required details')
		except IntegrityError:
			print('Integrity Error.')
			raise exceptions.PermissionDenied(detail='Username already exists')


#view all userprofiles present in the database
class ViewUserProfiles(APIView):
	def get(self,request,format=None):
		myuserprofile = MyUserProfile()
		serailizer_class = MyUserProfile.get_public_serializer()
		serialized_data = serailizer_class(myuserprofile.get_all_details(),many=True)
		return Response(serialized_data.data)

#view all questions present in the database
class ViewQuestions(APIView):
	def get(self,request,format=None):
		myquestion = MyQuestion()
		serailizer_class = MyQuestion.get_public_serializer()
		serialized_data = serailizer_class(myquestion.get_all_details(),many=True)
		return Response(serialized_data.data)

#view all comments present in the database
class ViewComments(APIView):
	def get(self,request,format=None):
		myquestioncomment = MyQuestionComment()
		serailizer_class = MyQuestionComment.get_public_serializer()
		serialized_data = serailizer_class(myquestioncomment.get_all_details(),many=True)
		return Response(serialized_data.data)

#view all images present in the database
class ViewImages(APIView):
	def get(self,request,format=None):
		myuserprofileimage = MyUserProfileImage()
		serailizer_class = MyUserProfileImage.get_public_serializer()
		serialized_data = serailizer_class(myuserprofileimage.get_all_details(),many=True)
		return Response(serialized_data.data)

#upload an image when user is signed in
class UploadImage(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,format=None):
		myuserprofileimage = MyUserProfileImage()
		return Response(myuserprofileimage.upload_new_image(user=request.user,data=request.data))

#view all comments for a particular question
class ViewQuestionAndComments(APIView):
	def get(self,request,id,format=None):
		myquestioncomment = MyQuestionComment()
		serailizer_class = MyQuestionComment.get_public_serializer()
		serialized_data = serailizer_class(myquestioncomment.get_question_comments(id=id),many=True)
		return Response(serialized_data.data)