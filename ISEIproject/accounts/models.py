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
    abbreviation = models.CharField(max_length=4, default=" ", help_text=' Enter the abbreviation for this school')
    school_code = models.CharField(max_length=15, help_text='Code to allow a user to register as principal',
                                   default="pxyughkn8986")
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

class SchoolYear(models.Model):
    name = models.CharField(max_length=9, unique=True)
    active_year = models.BooleanField(default=False)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(SchoolYear, self).save(*args, **kwargs)
        if self.active_year:
            all=SchoolYear.objects.exclude(id=self.id).update(active_year=False)


class PDARecord(models.Model):
    #entered by teacher at object creation
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=False, blank=False)
    school_year = models.ForeignKey(SchoolYear, null=True, blank=True, on_delete =models.PROTECT)

    class Meta:
        unique_together = ('teacher', 'school_year',)
        ordering = ['school_year']
    #entered by teacher at object finalization
    summary = models.CharField(validators=[MinLengthValidator(1)], max_length=3000, blank=True, null=True,
                               help_text='Summarize what you have learned from the combined activities and how you '
                                         'plan to apply this learning to your classroom')
    date_submitted = models.DateField(null=True, blank=True)
    #principal, after it's submitted
    principal_signature = models.BooleanField(null=False, default = False, blank=True)
    #ISEI admin, after signed by principal
    total_approved_ceus = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class PDAInstance(models.Model):
    #teacher
    pda_record = models.ForeignKey(PDARecord, on_delete=models.PROTECT, null=False, blank=False)
    pda_type = models.ForeignKey(PDAType, on_delete=models.PROTECT, null=False, blank=False)
    date_completed = models.DateField(null=False)
    description = models.CharField(validators=[MinLengthValidator(1)], max_length=3000, blank=False, null=False)
    # OR between those three
    ceu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    clock_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    pages = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    #ISEI admin
    CHOICES = (
        ('None', 'Pending'),
        ('True', 'Approved'),
        ('False', 'Not Approved'),
    )
    approved = models.NullBooleanField(choices = CHOICES, default = None)
    approval_comment = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering =['pda_record']
    @property
    def approved_ceu(self):
        if self.approved:
            if self.ceu is not None:
                return self.ceu
            elif self.pages is not None:
                return round(self.pages / 100, 2)
            elif self.clock_hours is not None:
                return round(self.clock_hours / 10, 2)

    def __str__(self):
        return self.description
