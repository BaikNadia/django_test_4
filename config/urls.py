from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dogs/', include('dogs.urls', namespace='dogs')),
    path('books/', include('library.urls', namespace='library')),
    path('users/', include('users.urls', namespace='users')),
    path('', RedirectView.as_view(url='books/', permanent=True), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
