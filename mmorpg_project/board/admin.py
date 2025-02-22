from django.contrib import admin
from .models import Advertisement, Response, Category, Newsletter, NewsletterSubscription

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'sent_at')
    search_fields = ('title', 'content')
    list_filter = ('sent_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at']
    list_filter = ['category', 'created_at']

admin.site.register(Response)
admin.site.register(NewsletterSubscription) 