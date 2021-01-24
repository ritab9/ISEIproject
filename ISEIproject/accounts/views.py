from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .filters import *
from .forms import *
from .utils import is_in_group


# authentication functions
@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # flash message (only appears once)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if is_in_group(request.user, 'teacher'):
                if user.date_joined.date() == user.last_login.date():
                    return redirect('account_settings')
                else:
                    return redirect('teacher_dashboard')
            if is_in_group(request.user, 'admin'):
                return redirect('admin_dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admindashboard(request):
    teachers = Teacher.objects.all()
    # TODO redo the dashboard, replace activity references
    activities = PDAInstance.objects.all()

    total_teachers = teachers.count()
    total_activities = activities.count()

    context = {'teachers': teachers, 'activities': activities, 'total_teachers': total_teachers,
               'total_activities': total_activities}
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacherdashboard(request):
    # TODO teacher dashboard
    teacher = request.user.teacher
    context = {'teacher': teacher}
    return render(request, 'accounts/teacher_dashboard..html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def accountsettings(request):
    # TODO account settings for different categories of users
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        teacher_form = TeacherForm(request.POST, request.FILES or None, instance=request.user.teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('account_settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        teacher_form = TeacherForm(instance=request.user.teacher)
    return render(request, 'accounts/account_settings.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })


# teacher activities for user with id=pk
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher', 'admin'])
def myPDA(request, pk):
    teacher = Teacher.objects.get(user=User.objects.get(id=pk))
    pda_records = PDARecord.objects.filter(teacher=teacher)
    pda_instance = PDAInstance.objects.filter(pda_record__in=pda_records)
    instance_filter = PDAInstanceFilter(request.GET, queryset=pda_instance)
    pda_instance = instance_filter.qs
    count = pda_instance.count()
    active_schoolyear = pda_records.filter(date_submitted__isnull=True).values('school_year')
    # if the logged in user is a teacher, teacher name will not be rendered in the website
    if is_in_group(request.user, 'teacher'):
        user_not_teacher = False
    else:
        user_not_teacher = True
    context = dict(teacher=teacher, user_not_teacher=user_not_teacher, active_schoolyear=active_schoolyear,
                   instance_filter=instance_filter, pda_instance=pda_instance, count=count)
    return render(request, 'accounts/myPDA.html', context)


# todo create layout in myPDA template for it to look nicer


# create activity record and instances (for teacher with matching pk)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def createPDA(request, pk):
    user = User.objects.get(id=pk)
    teacher = Teacher.objects.get(user=user)
    pdarecord = PDARecord()
    pdarecord.teacher = teacher
    pdarecord_form = PDARecordForm(instance=pdarecord)

    PDAInstanceFormSet = inlineformset_factory(PDARecord, PDAInstance, exclude=(),
                                               fields=(
                                                   'date_completed', 'pda_type', 'description', 'pages', 'clock_hours',
                                                   'ceu'),
                                               extra=1)

    pdainstance_formset = PDAInstanceFormSet(queryset=PDAInstance.objects.none(), instance=pdarecord)

    if request.method == 'POST':
        pdarecord_form = PDARecordForm(request.POST)
        pdainstance_formset = PDAInstanceFormSet(request.POST, request.FILES)

        if pdarecord_form.is_valid():
            created_pdarecord = pdarecord_form.save(commit=False)
            pdainstance_formset = PDAInstanceFormSet(request.POST, request.FILES, instance=created_pdarecord)

            if pdainstance_formset.is_valid():
                created_pdarecord.save()
                pdainstance_formset.save()
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                    if group == 'teacher':
                        # teacher landing page
                        return redirect('teacher_dashboard')
                    else:
                        # admin landing page
                        return redirect('admin_dashboard')

    context = {'teacher': teacher, 'pdarecord_form': pdarecord_form, 'pdainstance_formset': pdainstance_formset}
    return render(request, "accounts/create_pda.html", context)


# all activities (for staff)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def activities(request):
    activities = Activity.objects.all()
    total_activities = activities.count()

    my_filter = ActivityFilter(request.GET, queryset=activities)
    activities = my_filter.qs

    context = {'activities': activities, 'total_activities': total_activities, 'my_filter': my_filter}
    return render(request, 'accounts/activities.html', context)


# all teachers (for staff)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def teachers(request):
    teachers = Teacher.objects.all()
    total_teachers = teachers.count()

    my_filter = TeacherFilter(request.GET, queryset=teachers)
    teachers = my_filter.qs

    context = {'teachers': teachers, 'total_teachers': total_teachers, 'my_filter': my_filter}
    return render(request, 'accounts/teachers.html', context)


# teacher activities for logged in user
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def myactivities(request):
    teacher = request.user.teacher
    activities = Activity.objects.filter(teacher=teacher)
    total_activities = activities.count()

    my_filter = ActivityFilterTeacher(request.GET, queryset=activities)
    activities = my_filter.qs

    context = dict(my_filter=my_filter, teacher=teacher, activities=activities, total_activities=total_activities)
    return render(request, 'accounts/teacher.html', context)


# individual teacher profile (for teacher with matching pk)
@login_required(login_url='login')
def teacher(request, pk):
    user = User.objects.get(id=pk)
    teacher = Teacher.objects.get(user=user)
    activities = Activity.objects.filter(teacher=teacher)
    total_activities = activities.count()

    my_filter = ActivityFilterTeacher(request.GET, queryset=activities)
    activities = my_filter.qs

    context = dict(myFilter=my_filter, teacher=teacher, activities=activities, total_activities=total_activities)
    return render(request, 'accounts/teacher.html', context)


# create activity (for staff)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createactivity(request):
    form = ActivityForm
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/activity_form.html", context)


# update activity (for staff)
@login_required(login_url='login')
def updateActivity(request, pk):
    activity = Activity.objects.get(id=pk)
    form = ActivityForm(instance=activity)

    if request.method == 'POST':
        print("got POST")
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            print("form is valid")
            form.save()
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'teacher':
                    # teacher landing page
                    return redirect('/myactivities')
                else:
                    # admin landing page
                    return redirect('/activities')

    context = {'form': form}
    return render(request, "accounts/activity_form.html", context)


# delete activity (for staff)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def deleteActivity(request, pk):
    activity = Activity.objects.get(id=pk)
    if request.method == "POST":
        activity.delete()
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'teacher':
                # teacher landing page
                return redirect('/myactivities')
            else:
                # admin landing page
                return redirect('activities')
    context = {'item': activity}
    return render(request, 'accounts/delete.html', context)


# create activity (for teacher with matching pk)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def createUserActivity(request, pk):
    ActivityFormSet = inlineformset_factory(Teacher, Activity, exclude=('id', 'teacher'),
                                            fields=('date', 'category', 'ceu', 'clock_Hours', 'pages', 'summary'),
                                            extra=1)
    user = User.objects.get(id=pk)
    teacher = Teacher.objects.get(user=user)
    formset = ActivityFormSet(queryset=Activity.objects.none(), instance=teacher)
    # form = ActivityRecordForm (initial = {'teacher':teacher})
    if request.method == 'POST':
        formset = ActivityFormSet(request.POST, instance=teacher)
        if formset.is_valid():
            formset.save()
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'teacher':
                    # teacher landing page
                    return redirect('/myactivities')
                else:
                    # admin landing page
                    return redirect('activities')

    context = {'teacher': teacher, 'formset': formset}
    return render(request, "accounts/activityuser_form.html", context)
