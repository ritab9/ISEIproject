
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

	path('register/', views.registerpage, name ='register'),
	path('login/', views.loginpage, name ='login'),
	path('logout/', views.logoutuser, name ='logout'),

    path('', views.home, name ="home"),
    path('user/', views.userpage, name='user_page'),
    path('account/', views.accountsettings, name='account'),
    path('myactivities/', views.myactivities, name='myactivities'),

    path('activities/', views.activities, name ="activities"),
    path('teachers/', views.teachers, name ="teachers"),
    path('teacher/<str:pk>/', views.teacher, name ="teacher"),
	path('activities/create_activity/', views.createactivity, name="create_activity"),

	# pk is the activity ID
    path('activities/update_activity/<str:pk>/', views.updateActivity, name="update_activity"),
    path('activities/delete_activity/<str:pk>/', views.deleteActivity, name="delete_activity"),

	path('activities/create_activityuser/<str:pk>/', views.createUserActivity, name="create_activityuser"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/password_reset.html"), name = "reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_complete.html"), name = "password_reset_complete"),    
]

