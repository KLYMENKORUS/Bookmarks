from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^account/", include("account.urls")),
    path('social-auth/', include("social_django.urls", namespace="social")),
    path("images/", include("images.urls", namespace="images")),
    path("posts/", include("posts.urls", namespace="posts")),
    path("chat/", include("chat.urls", namespace="chat"))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
