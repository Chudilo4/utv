import re

from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, DeleteView, ListView
from django.views.generic.edit import FormMixin

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


class HomeView(TemplateView):
    template_name = 'utv_smeta/base.html'


class CardsListView(ListView):
    template_name = 'utv_smeta/cards.html'
    model = Cards

    def get_queryset(self):
        return Cards.objects.filter(author=self.request.user).union(Cards.objects.filter(performers=self.request.user))


class CardsCreateView(CreateView):
    form_class = CardsCreateForm
    template_name = 'utv_smeta/cards_create.html'
    success_url = reverse_lazy('cards')

    def get_form_kwargs(self):
        kwargs = super(CardsCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CardDetailView(DetailView):
    model = Cards
    template_name = 'utv_smeta/cards_detail.html'




class WorkerCreateUpdateView(View):
    def post(self, request, *args, **kwargs):
        form = WorkerForm(request.POST)
        pk = kwargs['pk']
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.card = Cards.objects.get(pk=pk)
            comment.save()
            return redirect('card_detail', pk=pk)
        return redirect('cards')


class CommentsAddView(View):
    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        pk = kwargs['pk']
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.card = Cards.objects.get(pk=pk)
            comment.save()
            return redirect('card_detail', pk=pk)
        return redirect('cards')


class WorkerDeleteView(DeleteView):
    model = Worker
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('card_detail', kwargs={'pk': self.get_object().card.pk})

