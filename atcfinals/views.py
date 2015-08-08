from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from rest_framework.views import APIView, Response, status 
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from rest_framework.authentication import TokenAuthentication

from .services import (MyInnovator,MyIdea,MyExperience,
	MyIdeaView,MyIdeaComment,MyIdeaLike)

@method_decorator(csrf_exempt)
def index(request):
	return render(request,'index2.html')

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
			user = User.objects.create_user(username=thisDict['username'],password=thisDict['password'])
			return Response('signup:successful')
		except KeyError:
			print('Key Error.')
			raise exceptions.ParseError(detail='Provide all required details')
		except IntegrityError:
			print('Integrity Error.')
			raise exceptions.PermissionDenied(detail='Username already exists')


class ViewInnovators(APIView):
	def get(self,request,format=None):
		myinnovator = MyInnovator()
		serializer_class = MyInnovator.get_public_serializer()
		serialized_data = serializer_class(myinnovator.get_all_details(),many=True)
		return Response(serialized_data.data)

class ViewInnovator(APIView):
	def get(self,request,id,format=None):
		myinnovator = MyInnovator()
		serializer_class = MyInnovator.get_public_serializer()
		serialized_data = serializer_class(myinnovator.get_innovator_detail(id=id))
		return Response(serialized_data.data)

class GetMyProfile(APIView):
	def get(self,request,format=None):
		if request.user.is_authenticated():
			myinnovator = MyInnovator()
			serializer_class = MyInnovator.get_public_serializer()
			serialized_data = serializer_class(myinnovator.get_my_details(user=request.user))
			return Response(serialized_data.data)
		else:
			raise exceptions.PermissionDenied(detail='Please log in to continue')

class ActionCreateInnovator(APIView):
	def post(self,request,format=None):
		myinnovator = MyInnovator()
		return Response(myinnovator.create_new_innovator(user=request.user,data=request.data))

class FindInnovatorsByKeyWord(APIView):
	def get(self,request,keyword,format=None):
		myinnovator = MyInnovator()
		serializer_class = MyInnovator.get_public_serializer()
		serialized_data = serializer_class(myinnovator.find_innovators_by_experience_keyword(keyword=keyword),many=True)
		return Response(serialized_data.data)

class ViewIdeas(APIView):
	#authentication_classes = (TokenAuthentication,)
	def get(self,request,format=None):
		if request.user.is_authenticated():
			print('User authenticated')
		else:
			print('User not authenticated')
		myidea = MyIdea()
		serializer_class = MyIdea.get_public_serializer()
		serialized_data = serializer_class(myidea.get_all_details(user=request.user),many=True)
		return Response(serialized_data.data)

class ViewIdea(APIView):
	def get(self,request,id,format=None):
		myidea = MyIdea()
		serializer_class = MyIdea.get_public_serializer()
		serialized_data = serializer_class(myidea.get_idea(user=request.user,id=id))
		return Response(serialized_data.data)

class PostIdea(APIView):
	def post(self,request,format=None):
		myidea = MyIdea()
		return Response(myidea.create_new_idea(user=request.user,data=request.data))

#class ViewIdeasdetail(APIView):
#	return Response('Coming soon.')

class ViewInnovatorExperiences(APIView):
	def get(self,request,id,format=None):
		myexperience = MyExperience()
		serializer_class = MyExperience.get_public_serializer()
		serialized_data = serializer_class(myexperience.get_innovator_experiences(id=id),many=True)
		return Response(serialized_data.data)

class ActionAddExperience(APIView):
	def post(self,request,format=None):
		myexperience = MyExperience()
		return Response(myexperience.create_experience(user=request.user,data=request.data))

#class ViewExperienceDetail(APIView):
#	return Response('Coming soon.')

class GetComments(APIView):
	def get(self,request,id,format=None):
		myideacomment = MyIdeaComment()
		serializer_class = MyIdeaComment.get_public_serializer()
		serialized_data = serializer_class(myideacomment.get_idea_comments(user=request.user,id=id),many=True)
		return Response(serialized_data.data)

class ActionComment(APIView):
	def post(self,request,id,format=None):
		myideacomment = MyIdeaComment()
		return Response(myideacomment.comment_on_idea(user=request.user,id=id,data=request.data))

class GetLikes(APIView):
	def get(self,request,id,format=None):
		myidealike = MyIdeaLike()
		serializer_class = MyIdeaLike.get_public_serializer()
		serialized_data= serializer_class(myidealike.get_idea_likers(user=request.user,id=id),many=True)
		return Response(serialized_data.data)	
	
class ActionLike(APIView):
	def post(self,request,id,format=None):
		myidealike = MyIdeaLike()
		return Response(myidealike.like_idea(user=request.user,id=id))



