from django.contrib import admin
from django.urls import path
from todo import views
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('profile/<int:user_id>', views.settings, name='settings'),
    path('current/', views.current, name='currenttodos'),
    path('create/', views.createtodo, name='createtodo'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('todo/<int:todo_id>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    path('delete/', views.delete_account, name='delete_account' ),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='todo/reset_password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='todo/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='todo/reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='todo/reset_password_done.html'), name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='todo/change_password.html'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='todo/change_password_done.html'), name='password_change_done'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
