from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import random, string

#generate random words
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

#store image in custom location
def user_profile_image_path(instance,filename):
	return '{0}/pictures/user_{1}/{2}{3}'.format(settings.MEDIA_ROOT,instance.user_relation.username, randomword(5), filename)


# Create your models here.

class Innovator(models.Model):
	user_relation = models.OneToOneField(User,help_text='Link Innovator to existing user account')#make primary key
	innovator_name = models.CharField(max_length=40,help_text='Enter you name here')
	innovator_email = models.EmailField(help_text='Enter you email address')
	innovator_bio_short = models.CharField(max_length=50,help_text='Tell about you in less than 50 characters')
	innovator_bio_long = models.CharField(max_length=500,help_text='Give us a summary about yourself')
	innovator_location = models.CharField(max_length=30,help_text='Where are you located?')
	innovator_webiste = models.URLField(null=True,blank=True,help_text='If you have a website or blog, please add the link here')
	views = models.IntegerField(default=0,editable=False,help_text='Number of views this profile has')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='When this profile was created')
	updated_at = models.DateTimeField(editable=False, auto_now=True,help_text='When this Innovator profile was last updated')
	innovator_picture = models.ImageField(null=True,blank=True,upload_to=user_profile_image_path)

	def __unicode__(self):
		return self.innovator_name


ACCEPTED_CATEGORIES = (
		("Education","Education"),
		("Technology","Technology"),
		("Finance","Finance"),
		("Agriculture","Agriculture"),
	)


class Idea(models.Model):
	identifier = models.AutoField(primary_key=True)
	innovator_relation = models.ForeignKey(Innovator,help_text='Which innovator owns this idea?')
	idea_name = models.CharField(max_length=40,help_text='What is the name of your idea?')
	idea_bio_short = models.CharField(max_length=50,help_text='In less than 50 characters, summarize your idea')
	idea_bio_long = models.CharField(max_length=500,help_text='Give a description of your idea in less than 500 words')
	idea_webiste = models.URLField(null=True,blank=True,help_text='Does your idea have a website?')
	is_public = models.BooleanField(help_text='Specify whether this idea will be public if true or only accessible by registered users')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='When this idea was added to the system')
	updated_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='When this idea was last updated')
	category = models.CharField(max_length=20,choices=ACCEPTED_CATEGORIES,help_text='Choose a category for your idea')
	likes = models.IntegerField(editable=False,default=0,help_text='Number of likes that this has. Only registed users can like')
	comments = models.IntegerField(editable=False,default=0,help_text='Number of comments that this idea has. Only registered users can comment')
	views_known = models.IntegerField(editable=False,default=0,help_text='Number of views that this idea has from registered users')
	views_unknown = models.IntegerField(editable=False,default=0,help_text='Number of view from anonymous users')
	idea_image = models.ImageField(null=True,blank=True,upload_to=user_profile_image_path)

	def __unicode__(self):
		return self.idea_name

class Experience(models.Model):
	innovator_relation = models.ForeignKey(Innovator,help_text='Innovator creating this experience event')
	start_date = models.DateField(help_text='Specify when this event started')
	end_date = models.DateField(help_text='Specify when this event ended')
	description = models.CharField(max_length=500,help_text='In not more than 500 words, describe this experience')
	skills_learnt = models.CharField(max_length=50,help_text='In less than 50 words, summarize what skills you gained through this event')#companies can use this to search for potential employees

	def __unicode__(self):
		return self.description

class IdeaView(models.Model):
	user_relation = models.ForeignKey(User,help_text='Registered user who is viewing this idea')
	idea_relation = models.ForeignKey(Idea,help_text='Idea being viewed')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='Time and date when this user viewed this idea')

class IdeaComment(models.Model):
	user_relation = models.ForeignKey(User, help_text='User who is commenting on the idea')
	idea_relation = models.ForeignKey(Idea,help_text='Idea being commented on')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='Date and time of first comment')
	updated_at = models.DateTimeField(editable=False,auto_now=True,help_text='Date and time of last update')
	comment_text = models.CharField(max_length=150,help_text='Comment in less than 150 characters')

	def __unicode__(self):
		return self.comment_text

class IdeaLike(models.Model):
	user_relation = models.ForeignKey(User,help_text='Registered user who is liking the idea')
	idea_relation = models.ForeignKey(Idea,help_text='Idea being liked')
	created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text='When this idea was liked by this user')

	class Meta:
		unique_together = ('user_relation','idea_relation')#prevents same user from liking the idea more than one time










