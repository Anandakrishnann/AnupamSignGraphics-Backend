from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('works', views.WorkViewSet, basename='work')
router.register('blogs', views.BlogViewSet, basename='blog')
router.register('gallery', views.GalleryViewSet, basename='gallery')
router.register('locations', views.LocationViewSet, basename='location')
router.register('services', views.ServiceViewSet, basename='service')

urlpatterns = [
    path('auth/login/', views.admin_login, name='admin-login'),
    path('settings/', views.site_settings, name='site-settings'),
    path('', include(router.urls)),
]
