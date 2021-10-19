from django.contrib import admin
from likes.models import Like


# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (
        'user',
        'content_type',
        'object_id',
        'content_object',
        'created_at',
    )
    list_filter = ('content_type',)
