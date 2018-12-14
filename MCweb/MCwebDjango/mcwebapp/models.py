from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User, on_delete=models.PROTECT,)
	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	# Override the __unicode__() method to return out something meaningful!
	# Remember if you use Python 2.7.x, define __unicode__ too!
	def __str__(self):
		return self.user.username

class TemplateFile(models.Model):
    name = models.CharField(max_length=30)
    upload_date = models.DateTimeField('date uploaded')
    file_name = models.FileField(upload_to='templateFiles/')
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class PDFFile(models.Model):
    name = models.CharField(max_length = 200)
    upload_date = models.DateTimeField('date uploaded')
    file_name = models.FileField(upload_to='pdfFiles/')
    template = models.ForeignKey(TemplateFile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class JSONFile(models.Model):
    name = models.CharField(max_length=30)
    upload_date = models.DateTimeField('date uploaded')
    file_name = models.FileField(upload_to='jsonFiles/')
    pdf = models.OneToOneField(PDFFile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class MatchPattern(models.Model):
    name = models.CharField(max_length=30)
    regex = models.CharField(max_length=60)
    template = models.ForeignKey(TemplateFile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

