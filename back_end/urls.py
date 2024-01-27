from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path("admin/", admin.site.urls),
               path("user/", include("user.urls")),
               path("project/", include("project.urls")),
               path("issues/", include("issue.urls")),
               path("chat/", include("chat.urls")),
               path("notification/", include("notification.urls")),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
