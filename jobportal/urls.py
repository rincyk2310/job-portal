"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/admin_loginpage/', admin.site.login, name='admin_loginpage'),
    path('', index,name='index'),
    path('admin_login', admin_login, name='admin_login'),
    path('user_login', user_login, name='user_login'),
    path('recruiter_login', recruiter_login, name='recruiter_login'),
    path('user_signup', user_signup, name='user_signup'),
    path('user_home', user_home, name='user_home'),
    path('Logout', Logout, name='Logout'),
    path('recruiter_signup', recruiter_signup, name='recruiter_signup'),
    path('recruiter_home', recruiter_home, name='recruiter_home'),
    path('admin_home', admin_home, name='admin_home'),
    path('view_users', view_users, name='view_users'),
    path('delete_user/<int:pid>', delete_user, name='delete_user'),
    path('recruiter_pending', recruiter_pending, name='recruiter_pending'),
    path('recruiter_accepted', recruiter_accepted, name='recruiter_accepted'),
    path('recruiter_rejected', recruiter_rejected, name='recruiter_rejected'),
    path('recruiter_all', recruiter_all, name='recruiter_all'),
    path('change_status/<int:pid>', change_status, name='change_status'),
    path('delete_recruiter/<int:pid>', delete_recruiter, name='delete_recruiter'),
    path('change_pwdadmin', change_pwdadmin, name='change_pwdadmin'),
    path('change_pwdrecruiter', change_pwdrecruiter, name='change_pwdrecruiter'),
    path('change_pwduser', change_pwduser, name='change_pwduser'),
    path('add_job', add_job, name='add_job'),
    path('job_list', job_list, name='job_list'),
    path('edit_job/<int:pid>', edit_job, name='edit_job'),
    path('change_companylogo/<int:pid>', change_companylogo, name='change_companylogo'),
    path('latest_jobs', latest_jobs, name='latest_jobs'),
    path('user_latestjob', user_latestjob, name='user_latestjob'),
    path('job_detail/<int:pid>', job_detail, name='job_detail'),
    path('applyjob/<int:pid>', applyjob, name='applyjob'),
    path('applied_candidates', applied_candidates, name='applied_candidates'),
    path('update-status/<int:pid>/<str:status>/', update_status, name='update_status'),
    path('contact', contact, name='contact'),
    path('search_jobs/', search_jobs, name='search_jobs'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('save-job/<int:pid>/', save_job, name='save_job'),
    path('saved-jobs/', saved_jobs, name='saved_jobs'),
    path('remove_savedjob/<int:id>/', remove_savedjob, name='remove_savedjob'),
    path('mailsent/', mail_sent),
    path('delete_job/<int:pid>/', delete_job, name='delete_job'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
