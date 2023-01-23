from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, DeleteView, ListView
from utv_smeta.forms import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from utv_smeta.models import Cards


# Create your views here.


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'utv_smeta/register_user.html'
    success_message = 'Вы зарегестриваны!'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        ProfileUser.objects.create(user_id=self.object.pk)
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'utv_smeta/login.html'
    form_class = AuthenticationForm


class ProfileUserView(DetailView):
    model = ProfileUser
    template_name = 'utv_smeta/profile_user.html'


class UpdateProfileView(UpdateView):
    form_class = ProfileUserForm
    template_name = 'utv_smeta/profile_user_update.html'
    model = ProfileUser

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profileuser.pk})


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('regiister')


class LogoutUserView(LogoutView):
    pass


class HomeView(TemplateView):
    template_name = 'utv_smeta/base.html'


class CardsListView(ListView):
    template_name = 'utv_smeta/cards.html'
    model = Cards

    def get_queryset(self):
        return Cards.objects.filter(Q(author=self.request.user) | Q(performers=self.request.user))


class CardsCreateView(CreateView):
    form_class = CardsCreateForm
    template_name = 'utv_smeta/cards_create.html'
    success_url = reverse_lazy('cards')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class CardDetailView(DetailView, CreateView):
    model = Cards
    template_name = 'utv_smeta/cards_detail.html'
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.card = self.get_object()
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('card_detail', kwargs={'pk': self.get_object().pk})






