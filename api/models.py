from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    business_name = models.CharField(max_length=200, default='Anupam Signgraphics')
    tagline = models.CharField(max_length=300, default='With the latest and most modern machinery')
    about_text = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    phone_1 = models.CharField(max_length=20, default='9447869398')
    phone_2 = models.CharField(max_length=20, default='7025858611')
    phone_3 = models.CharField(max_length=20, default='8129411991')
    whatsapp = models.CharField(max_length=20, default='9447869398')
    email = models.EmailField(blank=True, default='')
    address = models.TextField(default='Vaikom, Kottayam, Kerala')
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.business_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Location(models.Model):
    name = models.CharField(max_length=100)
    maps_url = models.URLField()
    address = models.CharField(max_length=300, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon_key = models.CharField(max_length=50, blank=True, help_text='Optional icon identifier')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Work(models.Model):
    CATEGORY_CHOICES = [
        ('flex', 'Flex & Boards'),
        ('led', '3D LED Letters'),
        ('wedding', 'Wedding & Invitation Cards'),
        ('uv', 'UV Flatbed'),
        ('cnc', 'CNC & Laser'),
        ('screen', 'Screen Printing'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='flex')
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='works/')
    client_name = models.CharField(max_length=150, blank=True)
    location_label = models.CharField(max_length=150, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'work'
            slug = base
            n = 1
            while Work.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class WorkImage(models.Model):
    work = models.ForeignKey(Work, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='works/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.work.title} image'


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=400, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'post'
            slug = base
            n = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('machine', 'Machinery'),
        ('shop', 'Shop'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Gallery images'

    def __str__(self):
        return self.title or f'{self.category} image'
