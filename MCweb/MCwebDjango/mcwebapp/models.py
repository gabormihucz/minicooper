from django.db import models
from django.contrib.auth.models import User


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


class PDFFile(models.Model):
    name = models.CharField(max_length = 200)
    upload_date = models.DateTimeField('date uploaded')
	file_ = models.FileField(upload_to='pdfFiles/')
	json = models.OneToOneField(JSONFile)

    def __str__(self):
        return self.name


class JSONFile(models.Model):
	name = models.CharField(max_length=30)
	upload_date = models.DateTimeField('date uploaded')
	file_ = models.FileField(upload_to='jsonFiles/')
	json = models.ForeignKey(PDFFile)

	def __str__(self):
        return self.name


class TemplateFile(models.Model):
	name = models.CharField(max_length=30)
	upload_date = models.DateTimeField('date uploaded')
	file_ = models.FileField(upload_to='templateFiles/')
	user = models.ForeignKey(User)

	def __str__(self):
        return self.name


class MatchPattern(models.Model):
	name = models.CharField(max_length=30)
	regex = models.CharField(max_length=60)
	template = models.ForeignKey(TemplateFile)

	def __str__(self):
        return self.name

