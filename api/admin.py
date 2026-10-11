from django.contrib import admin
from .models import SiteSettings, Location, Service, Work, WorkImage, Blog, GalleryImage


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'phone_1', 'whatsapp', 'updated_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_primary', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_published', 'created_at')
    list_filter = ('category', 'is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [WorkImageInline]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
