from django.urls import path, include
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
    UserDetailAPIView,
    UserRegisterAPIView,
    TableDetailAPIView,
    TableUpdateFactAPIView,
    TableUpdatePlannedAPIView,
    ExcelAPIView,
    ExcelDetailAPIView, CategoryEventAPIView, CategoryEventDetailAPIView, EventCalendarAPIView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
    path('users/', UsersReadAPIView.as_view(),
         name='users_list'),
    path('users/register/', UserRegisterAPIView.as_view(),
         name='users_register'),
    path('users/<int:user_pk>/', UserDetailAPIView.as_view(),
         name='users_detail'),
    path('cards/', CardsListAPIView.as_view(),
         name='cards_list'),
    path('cards/<int:card_pk>/', CardsDetailAPIView.as_view(),
         name='cards_detail'),
    path('cards/<int:card_pk>/comment/', CommentListAPIView.as_view(),
         name='comment_list'),
    path('cards/<int:card_pk>/comment/<int:com_pk>/', CommentDetailAPIView.as_view(),
         name='comment_detail'),
    path('cards/<int:card_pk>/worker/', WorkerListAPIView.as_view(),
         name='worker_list'),
    path('cards/<int:card_pk>/worker/<int:work_pk>/', WorkerDetailAPIView.as_view(),
         name='worker_detail'),
    path('cards/<int:card_pk>/table/', TableListAPIView.as_view(),
         name='table_list'),
    path('cards/<int:card_pk>/table/<int:table_pk>/', TableDetailAPIView.as_view(),
         name='table_detail'),
    path('cards/<int:card_pk>/table/<int:table_pk>/update_fact/', TableUpdateFactAPIView.as_view(),
         name='table_update_fact'),
    path('cards/<int:card_pk>/table/<int:table_pk>/update_planned/',
         TableUpdatePlannedAPIView.as_view(),
         name='table_update_planned'),
    path('cards/<int:card_pk>/table/<int:table_pk>/excel/',
         ExcelAPIView.as_view(),
         name='table_excel'),
    path('cards/<int:card_pk>/table/<int:table_pk>/excel/<int:excel_pk>/',
         ExcelDetailAPIView.as_view(),
         name='excel_detail'),
    path('category/event/', CategoryEventAPIView.as_view(), name='category_event'),
    path('event/categore/<int:cat_event_pk>/', CategoryEventDetailAPIView.as_view(), name='category_detail'),
    path('event/', EventCalendarAPIView.as_view(), name='event_list')

]
