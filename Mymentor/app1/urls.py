from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('students', views.students, name='students'),
    path('courses', views.courses, name='courses'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('detailcourse/<int:value>', views.detailcourse, name='detailcourse'),
    path('editcourse/<int:value>', views.editcourse, name='editcourse'),
    path('editstatus/<int:value>/<int:vale>', views.editstatus, name='editstatus'),
    path('list/<int:value>/<int:vale>', views.list, name='list'),
 	
 	
]