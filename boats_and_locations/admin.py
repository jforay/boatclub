from django.contrib import admin
from .models import Boat, Marina, MarinaPhoto


class MarinaPhotoInline(admin.TabularInline):
    model = MarinaPhoto
    extra = 3  # shows 3 empty photo slots by default


class MarinaAdmin(admin.ModelAdmin):
    inlines = [MarinaPhotoInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'lake', 'state', 'address', 'slug', 'display_states')
        }),
        ('Owner Contact', {
            'fields': ('owner_name', 'owner_phone', 'owner_email'),
            'description': 'Displayed in the footer of this location\'s page.',
        }),
        ('Media', {
            'fields': ('hero_image', 'carousel_image', 'video_url', 'checkfront_url'),
        }),
        ('Description', {
            'fields': ('description',),
        }),
        ('Restaurant', {
            'fields': ('restaurant_name', 'restaurant_description', 'restaurant_image'),
            'classes': ('collapse',),
        }),
        ('Feature Section', {
            'fields': ('feature_title', 'feature_description', 'feature_image'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Boat)
admin.site.register(Marina, MarinaAdmin)