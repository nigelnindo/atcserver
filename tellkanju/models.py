from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import random, string

#randomize image url
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def test_image_path(instance,filename):
	return '{0}/testImages/{1}{2}'.format(settings.MEDIA_ROOT,randomword(5),filename)


class Report(models.Model):
	id_number = models.CharField(max_length=20,help_text='ID of uploader',default='No id')
	description = models.CharField(max_length=200,help_text='Describe the report')
	reportedImage = models.ImageField(upload_to=test_image_path,help_text='Image addded to the report')
	latitude = models.CharField(max_length=30,help_text='Latitude coordinates')
	longitude = models.CharField(max_length=30,help_text='Longitude coordinates')

	def __unicode__(self):
		return self.description