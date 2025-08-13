# core/admin.py
from django.contrib import admin
from .models import User, Course, Offer, Purchase
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Extra', {'fields': ('role',)}),
    )

admin.site.register(Course)
admin.site.register(Offer)
admin.site.register(Purchase)
