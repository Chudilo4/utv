from django.urls import path
from utv_smeta.views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='regiister'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', ProfileUserView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='prpfile_update'),
    path('', HomeView.as_view(), name='home'),
    path('cards/', CardsListView.as_view(), name='cards'),
    path('card/create/', CardsCreateView.as_view(), name='card_create'),
    path('card/<int:card_pk>/', CardDetailView.as_view(), name='card_detail'),
    path('card/<int:card_pk>/update/', CardUpdateView.as_view(), name='card_update'),
    path('card/<int:card_pk>/delete/', CardDeleteView.as_view(), name='card_delete'),
    path('card/<int:card_pk>/worker/create/', WorkerCreateView.as_view(), name='worker_create'),
    path('card/<int:card_pk>/worker/update/', WorkerUpdateView.as_view(), name='worker_update'),
    path('card/<int:card_pk>/worker/delete/', WorkerDeleteView.as_view(), name='worker_delete'),
    path('card/<int:card_pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('card/<int:card_pk>/coment/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('card/<int:card_pk>/table/create/', TableCreateView.as_view(), name='table_create'),
    path('card/<int:card_pk>/table/<int:table_pk>/', TableDetailView.as_view(), name='table_detail'),
    path('card/<int:card_pk>/table/<int:table_pk>/updated/', TableUpdateView.as_view(), name='table_update'),
    path('card/<int:card_pk>/table/<int:table_pk>/update/planned/', TablePlannedUpdateView.as_view(), name='table_planned_update'),


]