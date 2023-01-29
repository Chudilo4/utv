from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('cards/', CardsAPIListView.as_view()),
    path('worker/', WorkerAPIListView.as_view()),
    path('profile/', ProfileUserListView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
