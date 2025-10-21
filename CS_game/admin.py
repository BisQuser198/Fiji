# CS_game/admin.py
from django.contrib import admin
from .models import Employee

# exposes the Employee table in admin & configures its display / list columns, search, filters
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department_id', 'manager_id', 'salary', 'promotable')  # columns shown in list view
    search_fields = ('name',)       # quick search box
    list_filter = ('promotable',)   # sidebar filter
# Now you can manage Employee records via Django admin interface
