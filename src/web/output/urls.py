from django.conf.urls import url
from django.conf.urls.static import static
from web import settings
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update/$', views.update, name='update'),
    url(r'^save_changes/$', views.save, name='save_changes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

