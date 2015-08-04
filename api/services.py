from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth

from rest_framework import serializers, exceptions

from .models import (UserProfile,Question,
		QuestionComment,UserProfileImage,ImageTests)

class UserSerializerPublic(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username','id')
		partial = True

class UserProfileSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	class Meta:
		model = UserProfile
		fields = ('description','user_relation')
		partial = True

class QuestionSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	class Meta:
		model = Question
		fields = ('user_relation','question_text','created_at','updated_at')

class QuestionCommentSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	question_relation = QuestionSerializerPublic()
	class Meta:
		model = QuestionComment
		fields = ('user_relation','question_relation','created_at','updated_at','comment_text')

class UserProfileImageSerializerPublic(serializers.ModelSerializer):
	owner = UserProfileSerializerPublic()
	image_url = serializers.SerializerMethodField()
	class Meta:
		model = UserProfileImage
		fields = ('image','owner','image_url','image_description')

	def get_image_url(self,obj):
		return obj.image.url

class ImageTestsSerializerPublic(serializers.ModelSerializer):
	class Meta:
		model = ImageTests
		fields = ('image','image_description')


class UserProfileImageInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfileImage
		fields = ('image','image_description')


class MyUserProfile:
	def __init__(self):
		self.viewset = UserProfile.objects.all()

	@staticmethod
	def get_public_serializer():
		return UserProfileSerializerPublic

	def get_all_details(self):
		return self.viewset

	#get details of innovator by id
	def get_user_details(self,id):
		try:
			single_instance = self.get_all_details().get(pk=id)
		except UserProfile.DoesNotExist:
			raise exceptions.NotFound(detail='User Profile with matching ID not found.')
		return single_instance

class MyQuestion:
	def __init__(self):
		self.viewset = Question.objects.all()

	@staticmethod
	def get_public_serializer():
		return QuestionSerializerPublic

	def get_all_details(self):
		return self.viewset

	#find a question according to its id
	def get_question_details(self,id):
		try:
			single_instance = self.get_all_details().get(pk=id)
		except Question.DoesNotExist:
			raise exceptions.NotFound(detail='Question with match ID not found')			
		return single_instance

	#find all questions that match a string
	def get_matching_questions(self,query_key):
		try:
			multiple_instances = self.get_all_details().filter(question_text__contains=query_key)
		except Question,DoesNotExist:
			raise exceptions.NotFound(detail='No match found')
		return multiple_instances

	#find all questions asked by a particular user by user id
	def get_user_questions(self,id):
		try:
			multiple_instances = self.get_all_details().filter(user_relation=id)
		except Question.DoesNotExist:
			raise exceptions.DoesNotExist(detail='User ID provided has no question in the database')
		return multiple_instances	

class MyQuestionComment:
	def __init__(self):
		self.viewset = QuestionComment.objects.all()

	@staticmethod
	def get_public_serializer():
		return QuestionCommentSerializerPublic

	def get_all_details(self):
		return self.viewset

	#get all comments on a particular question by question id
	def get_question_comments(self,id):
		try:
			multiple_instances = self.get_all_details().filter(question_relation=id)
		except QuestionComment.DoesNotExist:
			raise exceptions.NotFound(detail='No comments found for question id supplied.')
		print('We have a result')
		return multiple_instances

	#find all comments made by a user by user id
	def get_user_comments(self):
		return self.get_all_details().filter(user_relation=id)


class MyUserProfileImage:
	def __init__(self):
		self.viewset = UserProfileImage.objects.all()

	@staticmethod
	def get_public_serializer():
		return UserProfileImageSerializerPublic

	@staticmethod
	def get_input_serializer():
		return UserProfileImageInputSerializer

	def get_all_details(self):
		return self.viewset

	def upload_new_image(self,user,data):
		if user == AnonymousUser:
			raise exceptions.NotAuthenticated(details="Please authenticate")
		serailizer_class = MyUserProfileImage.get_input_serializer()
		serailized_data = serailizer_class(data=data)
		if serailized_data.is_valid():
			image = serailized_data.data.get('image')
			image_description = serailized_data.data.get('image_description')
			UserProfileImage.objects.create(owner=user.userprofile,image=image,image_description=image_description)
			return serailized_data.data
		return serailized_data.errors


class MyImageTests:
	def __init__(self):
		self.viewset = ImageTests.objects.all()

	@staticmethod
	def get_public_serializer():
		return ImageTestsSerializerPublic

	@staticmethod
	def get_input_serializer():
		return ImageTestsSerializerPublic

	def get_all_details(self):
		return self.viewset

	def upload_new_image(self,data):
		print('upload_new_image_function_called')
		print(data)
		serailizer_class = MyImageTests.get_input_serializer()
		serailized_data = serailizer_class(data=data)
		if serailized_data.is_valid():
			print('serializer data is valid.')
			image = serailized_data.data.get('image')
			print('Success uploading image')
			return ('upload:success')
		else:
			print(serailized_data.errors)
			raise exceptions.ParseError(detail=serailized_data.errors)











