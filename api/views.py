from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import SiteSettings, Location, Service, Work, WorkImage, Blog, GalleryImage
from .serializers import (
    AdminLoginSerializer,
    SiteSettingsSerializer,
    LocationSerializer,
    ServiceSerializer,
    WorkListSerializer,
    WorkDetailSerializer,
    WorkWriteSerializer,
    WorkImageSerializer,
    BlogListSerializer,
    BlogDetailSerializer,
    GalleryImageSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def admin_login(request):
    serializer = AdminLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    })


@api_view(['GET', 'PATCH'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def site_settings(request):
    settings_obj = SiteSettings.get_solo()

    if request.method == 'GET':
        return Response(SiteSettingsSerializer(settings_obj, context={'request': request}).data)

    if not (request.user and request.user.is_authenticated and request.user.is_staff):
        return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = SiteSettingsSerializer(
        settings_obj,
        data=request.data,
        partial=True,
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class WorkViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Work.objects.all()
        if self.action in ('list', 'retrieve') and not (
            self.request.user and self.request.user.is_authenticated and self.request.user.is_staff
        ):
            qs = qs.filter(is_published=True)
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')
        if category:
            qs = qs.filter(category=category)
        if featured == '1':
            qs = qs.filter(is_featured=True)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return WorkWriteSerializer
        return WorkDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser], parser_classes=[MultiPartParser, FormParser])
    def add_image(self, request, slug=None):
        work = self.get_object()
        serializer = WorkImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(work=work)
        return Response(WorkImageSerializer(serializer.instance, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)', permission_classes=[IsAdminUser])
    def delete_image(self, request, slug=None, image_id=None):
        work = self.get_object()
        try:
            image = work.images.get(pk=image_id)
        except WorkImage.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Blog.objects.all()
        if self.action in ('list', 'retrieve') and not (
            self.request.user and self.request.user.is_authenticated and self.request.user.is_staff
        ):
            qs = qs.filter(is_published=True)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        return BlogDetailSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = GalleryImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = GalleryImage.objects.all()
        if self.action in ('list', 'retrieve') and not (
            self.request.user and self.request.user.is_authenticated and self.request.user.is_staff
        ):
            qs = qs.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Service.objects.all()
        if self.action in ('list', 'retrieve') and not (
            self.request.user and self.request.user.is_authenticated and self.request.user.is_staff
        ):
            qs = qs.filter(is_active=True)
        return qs
