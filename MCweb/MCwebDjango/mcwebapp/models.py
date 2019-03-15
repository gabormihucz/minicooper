from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


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
    upload_date = models.DateTimeField('date uploaded', null=True)
    file_name = models.FileField(upload_to='templateFiles/', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class PDFFile(models.Model):
    name = models.CharField(max_length = 200)
    upload_date = models.DateTimeField('date uploaded', null=True)
    file_name = models.FileField(upload_to='pdfFiles/', null=True)
    template = models.ForeignKey(TemplateFile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class JSONFile(models.Model):
    name = models.CharField(max_length=30)
    upload_date = models.DateTimeField('date uploaded', null=True)
    file_name = models.FileField(upload_to='jsonFiles/', null=True)
    pdf = models.OneToOneField(PDFFile, on_delete=models.CASCADE, null=True)
    mandatory_fulfilled = models.BooleanField(null=True)
    status_string = models.CharField(max_length=4, default='Pass')
    slug = models.SlugField(null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(JSONFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name





class MatchPattern(models.Model):
    regex = models.CharField(max_length=60, null=True)
    # if a template is deleted, delete all its match patterns too
    template = models.ForeignKey(TemplateFile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.regex
