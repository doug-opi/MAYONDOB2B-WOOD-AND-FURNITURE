#from django.urls import path
#from . import views

#app_name = "accounts"
#urlpatterns = [
#    path('login/', views.CustomLoginView.as_view(), name='login'),
#    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

#    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
#    path('attendant/dashboard/', views.AttendantDashboardView.as_view(), name='attendant_dashboard'),
#    path('manager/create-attendant/', views.CreateAttendantView.as_view(), name='create_attendant'),

    # Password reset
#    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
#    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
#    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
#]
#from django.urls import path
#from django.contrib.auth import views as auth_views
#from . import views

#app_name = 'accounts'

#urlpatterns = [
    # Login / Logout
#    path('login/', views.CustomLoginView.as_view(), name='login'),
#    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Password Reset Flow
#    path('password-reset/', 
#         views.CustomPasswordResetView.as_view(), 
 #        name='password_reset'),

 #   path('password-reset/done/', 
 #        auth_views.PasswordResetDoneView.as_view(
 #            template_name='accounts/password_reset_done.html'
 #        ), 
 #        name='password_reset_done'),

 #   path('reset/<uidb64>/<token>/',
 #        auth_views.PasswordResetConfirmView.as_view(
 #            template_name='accounts/password_reset_confirm.html'
  #       ), 
 #        name='password_reset_confirm'),

 #   path('reset/done/',
 #        auth_views.PasswordResetCompleteView.as_view(
 #            template_name='accounts/password_reset_complete.html'
 #        ), 
 #        name='password_reset_complete'),
    # Dashboards
 #   path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
 #   path('attendant/dashboard/', views.AttendantDashboardView.as_view(), name='attendant_dashboard'),

    # Manager creates attendants
 #   path('manager/create-attendant/', views.CreateAttendantView.as_view(), name='create_attendant'),

    # Dashboards
    #path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    #path('attendant/dashboard/', views.AttendantDashboardView.as_view(), name='attendant_dashboard'),
#]
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Dashboards
    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('attendant/dashboard/', views.AttendantDashboardView.as_view(), name='attendant_dashboard'),

    # Manager creates attendants
    path('manager/create-attendant/', views.CreateAttendantView.as_view(), name='create_attendant'),
]

#<!--<p>Forgot your password? <a href="{% url 'accounts:password_reset' %}">Reset it here</a>.</p>-->
# <a href="{% url 'receipt_list' %}" target="attendant_iframe">🧾 View All Receipts</a>