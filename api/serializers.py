from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (
    SiteSettings, Location, Service, Work, WorkImage, Blog, GalleryImage,
)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ['id', 'image', 'caption', 'order', 'work']
        read_only_fields = ['work']


class WorkListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'category', 'short_description',
            'cover_image', 'cover_image_url', 'client_name', 'location_label',
            'is_featured', 'created_at',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None


class WorkDetailSerializer(serializers.ModelSerializer):
    images = WorkImageSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'category', 'short_description', 'description',
            'cover_image', 'cover_image_url', 'client_name', 'location_label',
            'is_featured', 'is_published', 'images', 'created_at', 'updated_at',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None


class WorkWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            'id', 'title', 'slug', 'category', 'short_description', 'description',
            'cover_image', 'client_name', 'location_label', 'is_featured', 'is_published',
        ]


class BlogListSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image', 'cover_image_url',
            'published_at',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None


class BlogDetailSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'cover_image',
            'cover_image_url', 'is_published', 'published_at', 'updated_at',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        if obj.cover_image:
            return obj.cover_image.url
        return None


class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'category', 'image', 'image_url', 'caption',
            'order', 'is_active', 'created_at',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        if obj.image:
            return obj.image.url
        return None


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'business_name', 'tagline', 'about_text', 'logo', 'logo_url',
            'phone_1', 'phone_2', 'phone_3', 'whatsapp', 'email', 'address',
            'hero_image', 'hero_image_url', 'locations', 'services', 'updated_at',
        ]
        read_only_fields = ['id', 'logo_url', 'hero_image_url', 'locations', 'services', 'updated_at']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        if obj.logo:
            return obj.logo.url
        return None

    def get_hero_image_url(self, obj):
        request = self.context.get('request')
        if obj.hero_image and request:
            return request.build_absolute_uri(obj.hero_image.url)
        if obj.hero_image:
            return obj.hero_image.url
        return None

    def get_locations(self, obj):
        qs = Location.objects.all()
        return LocationSerializer(qs, many=True).data

    def get_services(self, obj):
        qs = Service.objects.filter(is_active=True)
        return ServiceSerializer(qs, many=True).data


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password'],
        )
        if not user or not user.is_staff:
            raise serializers.ValidationError('Invalid admin credentials.')
        attrs['user'] = user
        return attrs
