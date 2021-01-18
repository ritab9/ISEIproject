from django.db import models
from django.db.models.functions import Round
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.core.validators import MinLengthValidator

# Create your models here.
class School(models.Model):
	name = models.CharField(max_length = 50, help_text = 'Enter the name of the school', unique = True)
	abbreviation = models.CharField (max_length = 4, default = "none", null = False, blank = False,  help_text = ' Enter the abbreviation for this school')
	principal = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, on_delete=models.SET_NULL)
	ordering = ['name']

	def __str__(self):
		return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete = models.CASCADE) 
    phone = models.CharField(max_length=20, null=True, blank = True) 
    profile_pic = models.ImageField(default = 'blank-profile.jpg', null=True, blank = True)
    school = models.ForeignKey(School, on_delete = models.PROTECT, null = True)
    CERTIFICATION_TYPES = {
		('v', 'Vocational'),
		('d', 'Designated'),
		('c', 'Conditional'),
		('e', 'Semi Professional'),
		('b', 'Basic'),
		('s', 'Standard'),
		('p', 'Professional'),
	}
    current_certification = models.CharField(max_length = 1, choices = CERTIFICATION_TYPES, help_text = "Choose a certification", null = True, blank = True)

    def __str__(self):
    	return self.user.last_name +', '+ self.user.first_name


class ActivityCategory(models.Model):
	detail = models.CharField( max_length = 100, help_text = 'Describe the possible activities', null = False)
	CATEGORIES = (
		('i', 'Independent'),
		('g', 'Group'),
		('c', 'Collaboration'),
		('p', 'Presentation & Writing'),
	)
	category = models.CharField(max_length = 1, choices = CATEGORIES, help_text = "Choose a category", null = False)
	typicalCEUvalue = models.CharField(max_length=60, null = True, blank = True)

	def __str__(self):
		return self.get_category_display() +' - '+self.detail

class Activity(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete = models.PROTECT, null=False, blank=False)
	date = models.DateField(null= False)
	category = models.ForeignKey(ActivityCategory, on_delete = models.PROTECT, null= False, blank = False)
	
	ceu = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
	clock_Hours = models.DecimalField(max_digits = 3, decimal_places = 1, null = True, blank = True)
	pages = models.DecimalField(max_digits = 3, decimal_places = 0, null = True, blank = True)
	
	@property
	def CEUs(self):
		if self.ceu != None:
			return self.ceu
		elif self.clock_Hours != None:
			return round(self.clock_Hours/10,2)
		elif self.pages != None:
			return round(self.pages/100,2)
	
	summary = models.CharField(validators=[MinLengthValidator(1)], max_length = 3000, blank = False, null = False, help_text = 'Summarize what you have learned from the combined activities and how you plan to apply this learning to your classroom')

	def __str__(self):
		return self.teacher.user.username+ ' activity'



