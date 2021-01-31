from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
'''
class EmployeeInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name_plural = 'users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
'''
class AccountAdmin(UserAdmin):
	list_display=('email','username','date_joined','last_login','is_admin','is_staff')
	search_fields=('email','username')
	readonly_fields=('date_joined','last_login')

	filter_horizontal=()
	list_filter=()
	fieldsets=()

admin.site.register(Items),
admin.site.register(Enrollment),
admin.site.register(Account,AccountAdmin)