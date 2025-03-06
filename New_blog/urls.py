from django.contrib import admin
from django.urls import path, include
from New_blog.blogApp.views import home
# from django.conf import settings
from .import settings
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('New_blog.blogApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include("New_blog.userApp.urls")),

]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

