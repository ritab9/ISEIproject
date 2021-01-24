from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #teacher urls
    path('teacherdashboard/', views.teacherdashboard, name='teacher_dashboard'),
    path('account_settings/', views.accountsettings, name='account_settings'),
    path('myPDA/<str:pk>', views.myPDA, name='myPDA'),

    path('update_pdainstance/<str:pk>/', views.updatePDAinstance, name="update_pdainstance"),
    path('delete_pdainstance/<str:pk>/', views.deletePDAinstance, name="delete_pdainstance"),

    path('create_pdainstance/<str:pk>', views.createPDAInstance, name='create_pdainstance'), #pk is for a pda record
    path('create_pda/<str:pk>', views.createPDA, name='create_pda'), #pk is for a teacher

    #admin urls
    path('admindashboard/', views.admindashboard, name='admin_dashboard'),




    path('activities/', views.activities, name="activities"),
    path('teachers/', views.teachers, name="teachers"),
    path('teacher/<str:pk>/', views.teacher, name="teacher"),
    path('activities/create_activity/', views.createactivity, name="create_activity"),

    # pk is the activity ID
    path('activities/create_activityuser/<str:pk>/', views.createUserActivity, name="create_activityuser"),



    # authentication urls
    path('', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),
]
