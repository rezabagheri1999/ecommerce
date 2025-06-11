from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (register, complete_profile, logout_page, custom_login_view, edit_profile, contact_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView
)
app_name = 'users'
urlpatterns = [
    # path('',include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('complete_profile/', complete_profile, name='complete_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/',logout_page,name = 'logout'),
    path('login/',custom_login_view,name = 'login'),
    path('contact/', contact_view, name='contact'),
    path('password-reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Password Change Flow (for logged-in users)
    path('password-change/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         CustomPasswordChangeDoneView.as_view(),
         name='password_change_done'),

]