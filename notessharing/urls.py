"""
URL configuration for notessharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('', views.index, name='index'),
    path('Notes', views.notes_details, name='notes_details'),
    path('Dashboard', views.dashboard, name='dashboard'),
    path('Login', views.login_view, name='login'),
    path('doLogin', views.do_login, name='doLogin'),
    path('doLogout', views.do_logout, name='logout'),
    path('usersignup/', views.user_signup, name='usersignup'),
    path('Profile', views.profile, name='profile'),
    path('Password', views.change_password, name='change_password'),
    path('AddNotes', views.add_notes, name='add_notes'),
    path('ManageNotes', views.manage_notes, name='manage_notes'),
    path('DeleteNOTES/<str:id>', views.delete_notes, name='delete_notes'),
     path('ViewNotes/<str:id>', views.view_notes, name='view_notes'),
     path('EditNotes', views.edit_notes, name='edit_notes'),
   path('SearchNotes', views.search_notes, name='search_notes'),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
