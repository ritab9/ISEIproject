from django.db import models
from django.db.models.functions import Round
from django.conf import settings
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinLengthValidator


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the school', unique=True, blank=False,
                            null=False)
    abbreviation = models.CharField(max_length=4, default="none", help_text=' Enter the abbreviation for this school')
    ordering = ['name']

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True, help_text="*Required")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(default='blank-profile.jpg', null=True, blank=True)

    CERTIFICATION_TYPES = {
        ('v', 'Vocational'),
        ('d', 'Designated'),
        ('c', 'Conditional'),
        ('e', 'Semi Professional'),
        ('b', 'Basic'),
        ('s', 'Standard'),
        ('p', 'Professional'),
    }
    current_certification = models.CharField(max_length=1, choices=CERTIFICATION_TYPES, null=True, blank=True)

    def __str__(self):
        return self.user.last_name + ', ' + self.user.first_name


class PDAType(models.Model):
    type = models.CharField(max_length=100, help_text='Describe the possible activities', null=False)
    CATEGORIES = (
        ('i', 'Independent'),
        ('g', 'Group'),
        ('c', 'Collaboration'),
        ('p', 'Presentation & Writing'),
    )
    category = models.CharField(max_length=1, choices=CATEGORIES, help_text="Choose a category", null=False)
    ceu_value = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.get_category_display() + ' - ' + self.type


class PDARecord(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=False, blank=False)
    school_year = models.CharField(max_length=9, null = True)
    summary = models.CharField(validators=[MinLengthValidator(1)], max_length=3000, blank=False, null = True,
                               help_text='Summarize what you have learned from the combined activities and how you '
                                         'plan to apply this learning to your classroom')
    date_submitted = models.DateField(default=datetime.now, null=True)
    principal_signature = models.BooleanField(null=True)



class PDAInstance(models.Model):
    pda_record = models.ForeignKey(PDARecord, on_delete=models.PROTECT, null=False, blank=False)
    pda_type = models.ForeignKey(PDAType, on_delete=models.PROTECT, null=False, blank=False)
    date_completed = models.DateField(null=False)
    description = models.CharField(validators=[MinLengthValidator(1)], max_length=3000, blank=False, null=False,
                                   help_text='Describe the activity')
    ceu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    clock_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    pages = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    approved = models.BooleanField(null=True)
    approval_comment = models.CharField(max_length=300, null=True)

    @property
    def approved_ceu(self):
        if self.approved:
            if self.ceu is not None:
                return self.ceu
            elif self.clock_hours is not None:
                return round(self.clock_hours / 10, 2)
            elif self.pages is not None:
                return round(self.pages / 100, 2)

    def __str__(self):
        return self.description
