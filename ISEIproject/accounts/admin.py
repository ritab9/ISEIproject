from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class TeacherInline(admin.StackedInline):
	model = Teacher
	max_num = 1
	can_delete = False

class UserAdmin(AuthUserAdmin):
	inlines = [TeacherInline]
	list_display = ('username','first_name', 'last_name')

admin.site.unregister(User) 
admin.site.register(User, UserAdmin)


@admin.register(School)
class School(admin.ModelAdmin):
	list_display = ('name','abbreviation', 'principal')
	fields = ['name', 'abbreviation', 'principal']
	

@admin.register(ActivityCategory)
class ActivityCategory(admin.ModelAdmin):
	list_display = ('category', 'detail','typicalCEUvalue')
	fields = ['category', 'detail', 'typicalCEUvalue']



@admin.register(Activity)
class Activity(admin.ModelAdmin):
	list_display = ('teacher', 'date')
	model = Activity

	