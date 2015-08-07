from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework import exceptions

from .models import (Innovator,Idea,
	Experience,IdeaView,IdeaComment,
	IdeaLike)


class UserSerializerPublic(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username','id')
		partial = True

class InnovatorSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	class Meta:
		model = Innovator
		fields = ('user_relation','innovator_name','innovator_email',
			'innovator_bio_short','innovator_bio_long','innovator_location',
			'innovator_webiste','views','innovator_picture')

class InnovatorInputSerializer(serializers.ModelSerializer):
	model = Innovator
	fields = ('pk','innovator_name','innovator_email',
			'innovator_bio_short','innovator_bio_long','innovator_location',
			'innovator_webiste','views','innovator_picture')

class IdeaSerializerPublic(serializers.ModelSerializer):
	innovator_relation = InnovatorSerializerPublic()
	class Meta:
		model = Idea
		fields = ('innovator_relation','idea_name','idea_bio_short',
			'idea_bio_long','idea_webiste','is_public','created_at',
			'updated_at','category','likes','comments','views_known',
			'views_unknown','idea_image','identifier')

class IdeaInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Idea
		fields = ('idea_name','idea_bio_short',
			'idea_bio_long','idea_webiste','is_public','created_at',
			'updated_at','category','likes','comments','views_known',
			'views_unknown','idea_image')

class ExperienceSerializerPublic(serializers.ModelSerializer):
	innovator_relation = InnovatorSerializerPublic()
	class Meta:
		model = Experience
		fields = ('innovator_relation','start_date','end_date','description',
			'skills_learnt')

class ExperienceInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Experience
		fields = ('start_date','end_date','description',
			'skills_learnt')

class IdeaViewSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	class Meta:
		fields = ('user_relation','idea_relation','created_at')

class IdeaCommentSerializerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	#idea_relation = IdeaSerializerPublic()#we don't need idea relation now
	class Meta:
		model = IdeaComment
		fields = ('user_relation','created_at','updated_at',
			'comment_text')

class IdeaCommentInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = IdeaComment
		fields = ('created_at','updated_at',
			'comment_text')

class IdeaLikeSerailizerPublic(serializers.ModelSerializer):
	user_relation = UserSerializerPublic()
	#idea_relation = IdeaSerializerPublic()#We don't need this for now
	class Meta:
		model = IdeaLike
		fields = ('user_relation','created_at')


class MyInnovator:
	def __init__(self):
		self.viewset = Innovator.objects.all()

	@staticmethod
	def get_public_serializer():
		return InnovatorSerializerPublic

	@staticmethod
	def get_input_serializer():
		return InnovatorInputSerializer

	def get_all_details(self):
		return self.viewset


	def get_my_details(self,user):
		try:
			single_instance = self.get_all_details().get(user_relation=user)
			return single_instance
		except Innovator.DoesNotExist:
			raise exceptions.NotFound(detail='Account may not be an innovator profile')

	#get details of one innovator by their username
	def get_innovator_detail(self,id):
		try:
			single_instance = self.get_all_details().get(user_relation__pk=id)
			single_instance.views += 1
			single_instance.save()
			return single_instance
		except Innovator.DoesNotExist:
			raise exceptions.NotFound(detail='Inovator does not exist.')

	#find innovators who match a keyword
	def find_innovators_by_experience_keyword(self,keyword):
		multiple_instance = self.get_all_details().filter(experience__skills_learnt__contains=keyword).distinct()
		return multiple_instance

	def create_new_innovator(self,user,data):
		print('created new innovator function called')
		if user.is_authenticated():
			print ('serializer is valid')
			try:
				thisDict = data.dict()
			except AttributeError:
				thisDict = data
			print('data turned into a dict')
			new_innovator = Innovator(user_relation = user,)
			if 'innovator_name' in thisDict:
				new_innovator.innovator_name = thisDict['innovator_name']
			else:
				raise exceptions.ParseError(detail='innovator_name required')
			if 'innovator_email' in thisDict:
				new_innovator.innovator_email = thisDict['innovator_email']
			else:
				raise exceptions.ParseError('innovator_email required')
			if 'innovator_bio_short' in thisDict:
				new_innovator.innovator_bio_short = thisDict['innovator_bio_short']
			else:
				raise exceptions.ParseError('innovator_bio_short')
			if 'innovator_bio_long' in thisDict:
				new_innovator.innovator_bio_long = thisDict['innovator_bio_long']
			else:
				raise exceptions.ParseError('innovator_bio_long required')
			if 'innovator_location' in thisDict:
				new_innovator.innovator_location = thisDict['innovator_location']
			else: 
				raise exceptions.ParseError('innovator_location required=True')
			if 'innovator_webiste' in thisDict:
				new_innovator.innovator_webiste = thisDict['innovator_webiste']
			if 'innovator_picture' in thisDict:
				new_innovator.innovator_picture = thisDict['innovator_picture']
			try:
				new_innovator.save()
			except IntegrityError:
				raise exceptions.PermissionDenied(detail='This account is already an innovators account')
			except Innovator.ValidationError:
				raise exceptions.ParseError(detail="Invalid form data submitted")
			return ('success:created new innovator')
		
			#raise exceptions.ParseError(details=serialized_data.errors)
		else:
			raise exceptions.PermissionDenied(detail='Log in to continue')


class MyIdea:
	def __init__(self):
		self.viewset = Idea.objects.all()

	@staticmethod
	def get_public_serializer():
		return IdeaSerializerPublic

	@staticmethod
	def get_input_serializer():
		return IdeaInputSerializer

	#refactored to handle both auth an anonymous users
	def get_all_details(self,user):
		if user.is_authenticated():
			multiple_instance = self.viewset
		else:
			multiple_instance = self.viewset.filter(is_public=True)
		return multiple_instance

	def get_idea(self,user,id):
		try:
			print('get_idea function called')
			single_instance = self.get_all_details(user=user).get(identifier=id)
			print('we got a single instance')
			if user == AnonymousUser:
				single_instance.views_unknown += 1
			else:
				single_instance = self.get_all_details(user=user).get(identifier=id)
				single_instance.views_known += 1
				view = IdeaView(user_relation=user,idea_relation=single_instance)
				view.save()
			single_instance.save()
			return single_instance 
		except Idea.DoesNotExist:
			raise exceptions.NotFound(detail='Idea not found')

	def create_new_idea(self,user,data):
		if user.is_authenticated():
			try:
				innovator = Innovator.objects.get(user_relation=user)
			except Innovator.DoesNotExist:
				raise exceptions.PermissionDenied(detail='Account type does not allow for this.')
			serializer_class = MyIdea.get_input_serializer()
			serialized_data = serializer_class(data=data)
			if serialized_data.is_valid():
				try:
					thisDict = data.dict()
				except AttributeError:
					thisDict = data
				new_idea = Idea(innovator_relation = innovator,
						idea_name = thisDict['idea_name'],
						idea_bio_short = thisDict['idea_bio_short'],
						idea_bio_long = thisDict['idea_bio_long'],
						category = thisDict['category']
						)
				if 'is_public' in thisDict:
					new_idea.is_public = thisDict['is_public']
				else:
					raise exceptions.ParseError(detail='Please specfy whether this idea is public or private')
				if 'idea_webiste' in thisDict:
					new_idea.idea_webiste = thisDict['idea_webiste']
				if 'idea_image' in thisDict:
					new_idea.idea_image = thisDict['idea_image']
				new_idea.save()
				return('success:idea added')
			else:
				raise exceptions.ParseError(detail=serialized_data.errors)
		else:
			raise exceptions.PermissionDenied(detail='Log in to continue')

class MyExperience:
	def __init__(self):
		self.viewset = Experience.objects.all()

	@staticmethod
	def get_public_serializer():
		return ExperienceSerializerPublic

	@staticmethod
	def get_input_serializer():
		return ExperienceInputSerializer

	def get_all_details(self):
		return self.viewset

	#not the best place to put this code
	def get_experience_with_keyword(self,keyword):
		return self.get_all_details().filter(skills_learnt__contains=keyword)

	def get_innovator_experiences(self,id):
		return self.get_all_details().filter(innovator_relation=id)

	def create_experience(self,user,data):
		if user.is_authenticated():
			try:
				innovator = Innovator.objects.get(user_relation=user)
			except Innovator.DoesNotExist:
				raise exceptions.PermissionDenied(detail='Account type does not allow for this')
			serializer_class = MyExperience.get_input_serializer()
			serialized_data = serializer_class(data=data)
			if serialized_data.is_valid():
				try:
					thisDict = data.dict()
				except AttributeError:
					thisDict = data
				new_experience = Experience(innovator_relation = innovator,
					start_date = thisDict['start_date'],
					end_date = thisDict['end_date'],
					description = thisDict['description'],
					skills_learnt = thisDict['skills_learnt'])
				new_experience.save()
				return ('sucess: new experience added')
			else:
				raise exceptions.ParseError(detail=serialized_data.errors)
		else:
			raise exceptions.PermissionDenied(detail='Please Log in')

class MyIdeaView:
	def __init__(self):
		self.viewset = IdeaView.objects.all()

	@staticmethod
	def get_public_serializer():
		return self.viewset

	def get_all_details(self,user):
		if user.is_authenticated():
			multiple_instance = self.viewset
		else:
			multiple_instance = self.viewset.filter(idea_relation__is_public=True)
		return multiple_instance

	def get_single_idea(self,user,id):
		return self.get_all_details(user=user).filter(pk=id)


class MyIdeaComment:
	def __init__(self):
		self.viewset = IdeaComment.objects.all()

	@staticmethod
	def get_public_serializer():
		return IdeaCommentSerializerPublic

	@staticmethod
	def get_input_serializer():
		return IdeaCommentInputSerializer

	def get_all_details(self,user):
		if user.is_authenticated():
			multiple_instance = self.viewset
		else:
			multiple_instance = self.viewset.filter(idea_relation__is_public=True)
		return multiple_instance

	def get_idea_comments(self,user,id):
		return self.get_all_details(user=user).filter(idea_relation=id)

	def comment_on_idea(self,user,id,data):
		if user.is_authenticated():
			serializer_class = MyIdeaComment.get_input_serializer()
			serialized_data = serializer_class(data=data)
			if serialized_data.is_valid():
				try:
					idea_instance = Idea.objects.all().get(pk=id)
				except Idea.DoesNotExist:
					raise exceptions.NotFound(detail='Idea not found')
				try:
					thisDict = data.dict()
				except AttributeError:
					thisDict = data
				new_comment = IdeaComment(
					user_relation = user,
					idea_relation = idea_instance,
					comment_text = thisDict['comment_text']
					)
				new_comment.save()
				idea_instance.comments += 1
				idea_instance.save()
				return ('succes:commented on idea')
			else:
				raise exceptions.ParseError(detail=serialized_data.errors)
		else:
			raise exceptions.PermissionDenied(detail='Please Log in')

class MyIdeaLike:
	def __init__(self):
		self.viewset = IdeaLike.objects.all()

	@staticmethod
	def get_public_serializer():
		return IdeaLikeSerailizerPublic

	def get_all_details(self,user):
		if user.is_authenticated():
			multiple_instance = self.viewset
		else:
			multiple_instance = self.viewset.filter(idea_relation__is_public=True)
		return multiple_instance

	def get_idea_likers(self,user,id):
		return self.get_all_details(user=user).filter(idea_relation=id)

	def like_idea(self,user,id):
		if user.is_authenticated():
			try:
				idea_instance = self.get_all_details(user=user).get(pk=id)
				new_like = IdeaLike(user_relation = user,
					idea_relation = idea_instance)
				new_like.save()
				idea_instance.likes += 1
				idea_instance.save()
				return('success:liked idea')
			except IdeaLike.DoesNotExist:
				raise exceptions.NotFound(detail='Idea not found.')
			except IdeaLike.IntegrityError:
				raise exceptions.PermissionDenied(detail='You have already liked this idea')
		else:
			raise exceptions.PermissionDenied(detail='Please Log In')





























