from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import (
    UsersReadAPIView,
    CardsListAPIView,
    CardsDetailAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    WorkerListAPIView,
    WorkerDetailAPIView,
    TableListAPIView,
    TablePlanedDetailAPIView,
    UserDetailAPIView,
    UserRegisterAPIView,
    WorkerAddAPIView,
    TableFactDetailAPIView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
    path('users/', cache_page(60)(UsersReadAPIView.as_view()),
         name='users_list'),
    path('users/register/', UserRegisterAPIView.as_view(),
         name='users_register'),
    path('users/<int:user_pk>/', cache_page(60)(UserDetailAPIView.as_view()),
         name='users_detail'),
    path('cards/', cache_page(60)(CardsListAPIView.as_view()),
         name='cards_list'),
    path('cards/<int:card_pk>/', cache_page(60)(CardsDetailAPIView.as_view()),
         name='cards_detail'),
    path('cards/<int:card_pk>/comment/', CommentListAPIView.as_view(),
         name='comment_list'),
    path('cards/<int:card_pk>/comment/<int:com_pk>/', CommentDetailAPIView.as_view(),
         name='comment_detail'),
    path('cards/<int:card_pk>/worker/', WorkerListAPIView.as_view(),
         name='worker_list'),
    path('cards/<int:card_pk>/worker/add/', WorkerAddAPIView.as_view(),
         name='worker_create'),
    path('cards/<int:card_pk>/worker/<int:work_pk>/', WorkerDetailAPIView.as_view(),
         name='worker_detail'),
    path('cards/<int:card_pk>/table/', TableListAPIView.as_view(),
         name='table_list'),
    path('cards/<int:card_pk>/table/<int:table_pk>/planned', TablePlanedDetailAPIView.as_view(),
         name='table_planned_detail'),
    path('cards/<int:card_pk>/table/<int:table_pk>/fact',
         TableFactDetailAPIView.as_view(), name='table_fact_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
