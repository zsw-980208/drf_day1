from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from drf_day1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userapp/', include("userapp.urls")),
    path('empapp/', include("empapp.urls")),
    path('stuapp/', include("stuapp.urls")),
    path('bookapp/', include("bookapp.urls")),
    path('day4/', include("drf_day4.urls")),
    url(r"^media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
]
