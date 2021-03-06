from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django_craiova.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_view'),
    path('users/', include('users.urls')),
    path('users/activate/', include('activation.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('payments/', include('payments.urls')),
    path('', view=homepage, name='homepage')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)