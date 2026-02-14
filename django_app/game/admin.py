from django.contrib import admin
from .models import Review, Report

# Register your models here.
admin.site.register(Review)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'user', 'reason', 'created_at', 'resolved')
    list_filter = ('reason', 'resolved')