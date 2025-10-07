from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('attendant/dashboard/', views.AttendantDashboardView.as_view(), name='attendant_dashboard'),
    path('manager/create-attendant/', views.CreateAttendantView.as_view(), name='create_attendant'),

    # Password reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
