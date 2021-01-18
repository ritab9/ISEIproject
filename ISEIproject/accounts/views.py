from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			# flash message (only appears once)
			messages.success(request, 'Account was created for '+ username)	
			return redirect('login')
	
	context={'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')	
		user = authenticate (request, username = username, password = password)
		
		if user is not None:
		 	login(request, user)
		 	#for new users go to account page
		 	if user.date_joined.date() == user.last_login.date():
		 		return redirect('account')
		 	else: 
		 		if request.user.groups.exists():
		 			group = request.user.groups.all()[0].name
		 			if group == 'teacher':
		 				#teacher landing page
		 				return redirect('user_page')
		 			else:
		 				#admin landing page
		 				return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context={}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


# this should be changed... it's pretty useless
@login_required(login_url = 'login')
@admin_only
def home(request):
	teachers = Teacher.objects.all()
	activities = Activity.objects.all()
	
	total_teachers = teachers.count()
	total_activities = activities.count()

	context = {'teachers': teachers, 'activities':activities, 'total_teachers':total_teachers, 'total_activities':total_activities}
	return render(request, 'accounts/home.html', context)


# all activities (for staff)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def activities(request):
	activities = Activity.objects.all()
	total_activities = activities.count()

	myFilter = ActivityFilter(request.GET, queryset = activities)
	activities = myFilter.qs

	context = {'activities':activities,'total_activities':total_activities, 'myFilter': myFilter}
	return render(request, 'accounts/activities.html', context)

# all teachers (for staff)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def teachers(request):
	teachers = Teacher.objects.all()
	total_teachers = teachers.count()

	myFilter = TeacherFilter(request.GET, queryset = teachers)
	teachers = myFilter.qs

	context = {'teachers': teachers, 'total_teachers':total_teachers, 'myFilter': myFilter}
	return render(request, 'accounts/teachers.html', context)

#teacher landing page, needs to be developed
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def UserPage(request):

	teacher = request.user.teacher
	context ={'teacher': teacher}
	return render(request, 'accounts/user.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def accountSettings(request):

	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		teacher_form = TeacherForm(request.POST, instance=request.user.teacher)
		if user_form.is_valid() and teacher_form.is_valid():
			user_form.save()
			teacher_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('account')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		user_form = UserForm(instance=request.user)
		teacher_form = TeacherForm(instance=request.user.teacher)
	return render(request, 'accounts/account_settings.html', {
		'user_form': user_form,
		'teacher_form': teacher_form
    })




# teacher activities for logged in user
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def myActivities(request):

	teacher = request.user.teacher
	activities = Activity.objects.filter(teacher = teacher)
	total_activities = activities.count()

	myFilter = ActivityFilterTeacher(request.GET, queryset = activities)
	activities = myFilter.qs


	context = {'myFilter': myFilter, 'teacher': teacher, 'activities':activities, 'total_activities':total_activities}
	return render(request, 'accounts/teacher.html', context)



# individual teacher profile (for teacher with maching pk)
@login_required(login_url = 'login')
def teacher(request, pk):
	user = User.objects.get(id = pk)
	teacher = Teacher.objects.get(user = user)
	activities = Activity.objects.filter(teacher = teacher)
	total_activities = activities.count()

	myFilter = ActivityFilterTeacher(request.GET, queryset = activities)
	activities = myFilter.qs


	context = {'myFilter': myFilter, 'teacher': teacher, 'activities':activities, 'total_activities':total_activities}
	return render(request, 'accounts/teacher.html', context)

#create activity (for staff)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def createActivity(request):
	form = ActivityForm
	if request.method =='POST':
		form = ActivityForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={'form':form}
	return render(request, "accounts/activity_form.html",context)

#update activity (for staff)
@login_required(login_url = 'login')
def updateActivity(request, pk):
	activity = Activity.objects.get(id=pk)
	form = ActivityForm(instance =activity)
	
	if request.method =='POST':
		print("got POST")
		form = ActivityForm(request.POST, instance=activity)
		if form.is_valid():
			print("form is valid")
			form.save()
			if request.user.groups.exists():
		 		group = request.user.groups.all()[0].name
		 		if group == 'teacher':
		 			#teacher landing page
		 			return redirect('/myactivities')
		 		else:
		 			#admin landing page
		 			return redirect('/activities')
			

	context={'form':form}
	return render(request, "accounts/activity_form.html",context)

#delete activity (for staff)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def deleteActivity(request,pk):
	activity = Activity.objects.get(id=pk)
	if request.method == "POST":
		activity.delete()
		if request.user.groups.exists():
		 			group = request.user.groups.all()[0].name
		 			if group == 'teacher':
		 				#teacher landing page
		 				return redirect('/myactivities')
		 			else:
		 				#admin landing page
		 				return redirect('activities')
	context={'item':activity}
	return render(request, 'accounts/delete.html', context)

#create activity (for teacher with matching pk)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def createUserActivity(request, pk):
	ActivityFormSet = inlineformset_factory(Teacher, Activity, exclude =('id','teacher'), fields = ('date', 'category', 'ceu', 'clock_Hours', 'pages','summary'), extra = 1)
	user = User.objects.get(id = pk)
	teacher = Teacher.objects.get(user = user)
	formset = ActivityFormSet(queryset = Activity.objects.none(), instance = teacher)
	#form = ActivityRecordForm (initial = {'teacher':teacher})
	if request.method =='POST':
		formset = ActivityFormSet(request.POST, instance = teacher)
		if formset.is_valid():
			formset.save()
			return redirect('/myactivities')

	context={'teacher':teacher,'formset':formset}
	return render(request, "accounts/activityuser_form.html",context)



