from django.contrib import admin
from .models import Employee


# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'e_no', 'e_name', 'e_sal', 'e_addr']


admin.site.register(Employee, EmployeeAdmin)
