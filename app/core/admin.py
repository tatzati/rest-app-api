from django.contrib import admin
from core.models import User
from core.models import Plan
from core.models import Workout
from core.models import Activity


class MyUser(admin.ModelAdmin):
    list_display = ('name', 'email')  # fields to display in the listing
    empty_value_display = '-empty-'  # display value when empty
    list_filter = ('email',)  # enable results filtering
    list_per_page = 25  # number of items per page
    ordering = ['email']  # Default results ordering


class MyPlan(admin.ModelAdmin):
    list_display = ('name',)  # fields to display in the listing
    empty_value_display = '-empty-'  # display value when empty
    list_filter = ('email',)  # enable results filtering
    list_per_page = 25  # number of items per page
    ordering = ['email']  # Default results ordering


class MyWorkout(admin.ModelAdmin):
    list_display = ('name', 'email')  # fields to display in the listing
    empty_value_display = '-empty-'  # display value when empty
    list_filter = ('email',)  # enable results filtering
    list_per_page = 25  # number of items per page
    ordering = ['email']  # Default results ordering


class MyActivity(admin.ModelAdmin):
    list_display = ('name', 'email')  # fields to display in the listing
    empty_value_display = '-empty-'  # display value when empty
    list_filter = ('email',)  # enable results filtering
    list_per_page = 25  # number of items per page
    ordering = ['email']  # Default results ordering


admin.site.register(User, MyUser)
admin.site.register(Plan)
admin.site.register(Workout)
admin.site.register(Activity)
