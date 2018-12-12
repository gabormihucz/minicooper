from django.db import models
from django.contrib.auth.models import User
"""
class PdfFile(models.Model):
    file_name = models.CharField(max_length = 200)
    upload_date = models.DateTimeField('date uploaded')

    def __str__(self):
        return self.file_name
"""
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	# Override the __unicode__() method to return out something meaningful!
	# Remember if you use Python 2.7.x, define __unicode__ too!
	def __str__(self):
		return self.user.username