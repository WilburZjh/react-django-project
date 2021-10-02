from django.contrib import admin
from models import Gender
from models import UserProfile
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('gender', 'text')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'gender', 'avatar', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
