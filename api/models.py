from django.db import models
from django.contrib.auth.models import User
# Create your models here.

import random, string

#randomize image url
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

#store image in custom location
def user_profile_image_path(instance,filename):
	return 'media/pictures/user_{0}/{1}{2}'.format(instance.owner.username, randomword(5), filename)

def test_image_path(instance,filename):
	return 'media/testImages/{0}{1}'.format(randomword(5),filename)

class UserProfile(models.Model):
	description = models.CharField(max_length=200,help_text='Give a summary of your individual expertise.')	
	user_relation = models.OneToOneField(User,help_text='Link to user profile',unique=True)
	def __unicode__(self):
		return self.user_relation.username

class Question(models.Model):
	user_relation = models.ForeignKey(User,help_text='User who created the question.')
	question_text = models.CharField(max_length=500,help_text='Enter your question here.')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='This is when this question was created')
	updated_at = models.DateTimeField(editable=False,auto_now=True,help_text='This is when this question was last updated')

	def __unicode__(self):
		return self.question_text

class QuestionComment(models.Model):
	user_relation = models.ForeignKey(User,help_text='The user who is making a comment')
	question_relation = models.ForeignKey(Question,help_text='The question being commented on')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='When this comment was added to the system')
	updated_at = models.DateTimeField(editable=False,auto_now=True)
	comment_text = models.CharField(max_length=300,help_text='Comment on a question')

	def __unicode__(self):
		return self.comment_text

class UserProfileImage(models.Model):
	owner = models.ForeignKey(UserProfile,help_text='Who uploaded the picture')
	image = models.ImageField(upload_to=user_profile_image_path,help_text='Link to uploaded picture')
	image_description = models.CharField(max_length=100,help_text='Describe this image',default='No description provided.')

	def __unicode__(self):
		return self.image.name

class ImageTests(models.Model):
	image = models.ImageField(upload_to=test_image_path)
	image_description = models.CharField(max_length=100,help_text='Describe this image')

	def __unicode__(self):
		return self.image.name