from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #teacher urls

    path('teacherdashboard/', views.teacherdashboard, name='teacher_dashboard'),
    path('account_settings/', views.accountsettings, name='account_settings'),
    path('myPDAdashboard/<str:pk>', views.myPDAdashboard, name='myPDAdashboard'),

    path('update_pdainstance/<str:pk>/', views.updatePDAinstance, name="update_pdainstance"),
    path('delete_pdainstance/<str:pk>/', views.deletePDAinstance, name="delete_pdainstance"),

    #create PDA instances and records. View submitted PDAs
    #new record: pk - user ID, 0, sy- School-year,  #existing record: 0 recId 0 PDA record ID
    path('create_pda/<str:pk>/<str:recId>/<str:sy>/', views.createPDA, name='create_pda'),


    #principal urls




    #admin urls
    path('admindashboard/', views.admindashboard, name='admin_dashboard'),



#Unused
#   path('teachers/', views.teachers, name="teachers"),
#    path('teacher/<str:pk>/', views.teacher, name="teacher"),
#    path('activities/create_activity/', views.createactivity, name="create_activity"),

    # pk is the activity ID
#   path('activities/create_activityuser/<str:pk>/', views.createUserActivity, name="create_activityuser"),



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
