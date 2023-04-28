from django.conf.urls.static import static
from django.urls import path

from OS_Project import settings
from Scheduler import views

urlpatterns = [
    path('', views.index, name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)