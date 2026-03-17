from django.contrib import admin
from .models import Boat, Marina, MarinaPhoto


class MarinaPhotoInline(admin.TabularInline):
    model = MarinaPhoto
    extra = 3  # shows 3 empty photo slots by default


class MarinaAdmin(admin.ModelAdmin):
    inlines = [MarinaPhotoInline]


admin.site.register(Boat)
admin.site.register(Marina, MarinaAdmin)