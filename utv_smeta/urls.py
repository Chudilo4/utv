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
    path('cards/create/', CardsCreateView.as_view(), name='card_create'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('cards/<int:pk>/worker/create/', WorkerCreateUpdateView.as_view(), name='worker_create'),
    path('worker/<int:pk>/update/', WorkerCreateUpdateView.as_view(), name='worker_update'),
    path('worker/<int:pk>/delete', WorkerDeleteView.as_view(), name='worker_delete')
]