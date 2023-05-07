from django.conf.urls.static import static
from django.urls import path

from OS_Project import settings
from Scheduler.views import Index, ShowLog

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('<int:pk>/', ShowLog.as_view(), name="showLog"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
